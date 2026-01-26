# Pharmacy Management System — Database Normalization (0NF → 3NF)

This document explains how the pharmacy schema in [python_backend/schema.sql](python_backend/schema.sql) satisfies First, Second, and Third Normal Forms by decomposing a practical, unnormalized retail sheet into well-structured tables.

## Assumed Initial Table (0NF — Unnormalized)
A typical POS/invoice spreadsheet might track an entire sale in one row with repeating groups:

- Columns: `invoice_no`, `date`, `customer_name`, `customer_phone`, `medicine_1`, `qty_1`, `price_1`, `batch_1`, `expiry_1`, `medicine_2`, `qty_2`, `price_2`, ... plus totals, tax, payment method, supplier, etc.
- Violations:
  - Repeating groups: multiple medicine columns per invoice row.
  - Multi-valued attributes: a single cell holds multiple values (e.g., skills-like lists → here, multiple medicines/batches).
  - Update anomaly: changing a batch price or expiry requires editing many rows.
  - Insert anomaly: you cannot add a new medicine/batch that hasn’t sold yet.
  - Delete anomaly: deleting the only sale of a batch erases the batch/medicine details.

## 1NF — Eliminate Repeating Groups, Ensure Atomic Values
We split the sheet into atomic columns; each cell holds a single value. Primary keys uniquely identify rows.

- Tables achieving 1NF (as defined in the schema):
  - `pharmacy(id, ...)` — one pharmacy profile.
  - `users(id, pharmacy_id, name, email, role, ...)` — atomic user attributes; one admin per pharmacy via index.
  - `suppliers(id, name, contact_person, email, phone, ...)` — one row per supplier.
  - `medicines(id, medicine_name, composition, uses, side_effects, manufacturer, price, category, ...)` — one row per medicine.
  - `inventory(id, medicine_id, batch_id, quantity, expiry_date, supplier_id, purchase_price, selling_price, barcode, ...)` — one row per medicine batch per supplier.
  - `customers(id, name, email, phone, address, ...)` — atomic customer fields.
  - `prescriptions(id, customer_id, doctor_name, prescription_date, ...)` — one row per prescription.
  - `orders(id, customer_id, prescription_id, total, status, ...)` — customer order header.
  - `sales(id, pharmacy_id, customer_id, invoice_number, subtotal, discount, tax, final_amount, payment_method, ...)` — invoice header; atomic amounts.
  - `sales_items(id, sale_id, medicine_id, inventory_id, quantity, unit_price, total_price, ...)` — one row per line item; no repeating groups.
  - `auth_tokens(id, user_id, token, expires_at, ...)` — session tokens per user.

Conclusion: Every table has a primary key and atomic attributes; 1NF is satisfied.

## 2NF — Remove Partial Dependencies
Rule: Table must be in 1NF and every non-key attribute must depend on the whole primary key (relevant when a table’s primary key is composite).

- Most tables use a surrogate primary key (`id`). Non-key attributes depend on that whole key by design.
- `sales_items` is conceptually identified by the composite business key `{sale_id, inventory_id}` (or `{sale_id, medicine_id, batch_id}`), though we also use a surrogate `id`. All non-key attributes (`quantity`, `unit_price`, `total_price`) depend on the full pair `{sale_id, inventory_id}` — not on just `sale_id` or just `inventory_id`.
- Join/lookup tables with composite natural keys could be declared with unique constraints to reflect this dependency (optional enforcement):
  - UNIQUE(sale_id, inventory_id)

Conclusion: There are no attributes that depend on only a part of a composite key; 2NF is satisfied.

## 3NF — Remove Transitive Dependencies
Rule: Table must be in 2NF and no non-key attribute should depend on another non-key attribute.

- `users`: non-key attributes (`name`, `email`, `role`, `status`) depend only on `id`. No attribute (e.g., `role`) determines others.
- `medicines`: descriptive columns depend only on `id`; `manufacturer` does not determine `price` or `category` within this design.
- `inventory`: batch details (`batch_id`, `expiry_date`, `supplier_id`, prices) depend on `id` and reference parents by FK; supplier/contact details live in `suppliers` and not here.
- `customers`: contact fields depend only on `id`; sales-specific data stays in `sales`.
- `sales`: header amounts and `payment_method` depend only on `id`; line specifics are in `sales_items`.
- `sales_items`: pricing and quantities depend on the item row; medicine metadata remains in `medicines` and batch data in `inventory`.
- `prescriptions`, `orders`, `auth_tokens`: each stores attributes that depend solely on its own primary key; cross-table details are referenced via FKs.

Conclusion: No non-key attribute is a determinant of another non-key attribute; 3NF is satisfied.

## Anomalies Prevented by the Design
- Update: Change a medicine’s description once in `medicines`; batch prices/expiry in `inventory`; customer phone in `customers` — no multi-row edits.
- Insert: Add new medicines or batches without any sale via `medicines`/`inventory`.
- Delete: Removing a stale sale does not remove medicine or batch definitions.

## Keys and Recommended Constraints (Summary)
- Primary Keys: `id` on each table (surrogate, SERIAL).
- Foreign Keys: 
  - `users.pharmacy_id → pharmacy.id`
  - `inventory.medicine_id → medicines.id`; `inventory.supplier_id → suppliers.id`
  - `sales.pharmacy_id → pharmacy.id`; `sales.customer_id → customers.id`; `sales.generated_by_user_id → users.id`
  - `sales_items.sale_id → sales.id`; `sales_items.inventory_id → inventory.id`; `sales_items.medicine_id → medicines.id`
  - `orders.customer_id → customers.id`; `orders.prescription_id → prescriptions.id`
  - `prescriptions.customer_id → customers.id`
  - `auth_tokens.user_id → users.id`
- Suggested Uniques (business keys):
  - `sales.invoice_number` (already UNIQUE)
  - `inventory(medicine_id, batch_id)` — a batch per medicine
  - `sales_items(sale_id, inventory_id)` — line uniqueness per sale

## Optional BCNF Considerations
- If business rules imply `barcode` uniquely identifies an `inventory` row, add `UNIQUE(barcode)` (index already present) and treat it as an alternate key.
- If a manufacturer should uniquely determine certain medicine attributes, model manufacturers in a separate table to remain in BCNF.

## Mapping to UI and APIs
- Product catalog and search: `medicines` + `inventory`.
- Cart/Invoice: `sales` (header) + `sales_items` (lines).
- Customer profiles: `customers`; prescriptions upload: `prescriptions`.
- Supplier management and purchasing: `suppliers`, `inventory`.
- Authentication and roles: `users`, `auth_tokens`, `pharmacy`.

This decomposition directly reflects the implemented schema and ensures 1NF, 2NF, and 3NF for robust, anomaly-free operations in the pharmacy system.
