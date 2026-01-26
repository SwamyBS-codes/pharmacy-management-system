import DashboardLayout from "@/components/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Plus, Edit2, Trash2 } from "lucide-react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";

interface Supplier {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  contact_person?: string;
  address?: string;
  created_at: string;
}

interface SupplierFormData {
  name: string;
  email: string;
  phone: string;
  contact_person: string;
  address: string;
}

const initialFormData: SupplierFormData = {
  name: "",
  email: "",
  phone: "",
  contact_person: "",
  address: "",
};

const validateForm = (data: SupplierFormData): string[] => {
  const errors: string[] = [];

  if (!data.name.trim()) {
    errors.push("Supplier name is required");
  }
  if (data.email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    errors.push("Please enter a valid email address");
  }
  if (!data.phone.trim()) {
    errors.push("Phone number is required");
  }
  if (!data.address.trim()) {
    errors.push("Address is required");
  }

  return errors;
};

export default function Suppliers() {
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [formData, setFormData] = useState<SupplierFormData>(initialFormData);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const { data: suppliers, isLoading, error, refetch } = useQuery<Supplier[]>({
    queryKey: ["suppliers"],
    queryFn: async () => {
      const response = await fetch("/api/suppliers");
      if (!response.ok) throw new Error("Failed to fetch suppliers");
      return response.json();
    },
  });

  // Create Supplier Mutation
  const createMutation = useMutation({
    mutationFn: async (data: SupplierFormData) => {
      const response = await fetch("/api/suppliers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: data.name,
          email: data.email || undefined,
          phone: data.phone,
          contact_person: data.contact_person || undefined,
          address: data.address,
        }),
      });
      if (!response.ok) throw new Error("Failed to create supplier");
      return response.json();
    },
    onSuccess: () => {
      toast({
        title: "Success",
        description: "Supplier created successfully",
        variant: "default",
      });
      refetch();
      handleDialogClose();
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to create supplier",
        variant: "destructive",
      });
    },
  });

  // Update Supplier Mutation
  const updateMutation = useMutation({
    mutationFn: async (data: SupplierFormData) => {
      const response = await fetch(`/api/suppliers/${editingId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: data.name,
          email: data.email || undefined,
          phone: data.phone,
          contact_person: data.contact_person || undefined,
          address: data.address,
        }),
      });
      if (!response.ok) throw new Error("Failed to update supplier");
      return response.json();
    },
    onSuccess: () => {
      toast({
        title: "Success",
        description: "Supplier updated successfully",
        variant: "default",
      });
      refetch();
      handleDialogClose();
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to update supplier",
        variant: "destructive",
      });
    },
  });

  // Delete Supplier Mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const response = await fetch(`/api/suppliers/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete supplier");
      return response.json();
    },
    onSuccess: () => {
      toast({
        title: "Success",
        description: "Supplier deleted successfully",
        variant: "default",
      });
      refetch();
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to delete supplier",
        variant: "destructive",
      });
    },
  });

  const handleDialogClose = () => {
    setIsDialogOpen(false);
    setFormData(initialFormData);
    setEditingId(null);
    setValidationErrors([]);
  };

  const handleAddSupplier = () => {
    setEditingId(null);
    setFormData(initialFormData);
    setValidationErrors([]);
    setIsDialogOpen(true);
  };

  const handleEditSupplier = (supplier: Supplier) => {
    setEditingId(supplier.id);
    setFormData({
      name: supplier.name,
      email: supplier.email || "",
      phone: supplier.phone || "",
      contact_person: supplier.contact_person || "",
      address: supplier.address || "",
    });
    setValidationErrors([]);
    setIsDialogOpen(true);
  };

  const handleDeleteSupplier = (id: number) => {
    if (confirm("Are you sure you want to delete this supplier?")) {
      deleteMutation.mutate(id);
    }
  };

  const handleSubmit = () => {
    const errors = validateForm(formData);

    if (errors.length > 0) {
      setValidationErrors(errors);
      toast({
        title: "Validation Error",
        description: errors[0],
        variant: "destructive",
      });
      return;
    }

    if (editingId) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear validation error for this field when user starts typing
    setValidationErrors((prev) =>
      prev.filter((error) => !error.toLowerCase().includes(name))
    );
  };

  if (isLoading) {
    return (
      <DashboardLayout title="Suppliers" subtitle="Manage supplier information">
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-600">Loading suppliers...</div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout title="Suppliers" subtitle="Manage supplier information">
        <div className="flex items-center justify-center h-64">
          <div className="text-red-600">
            Error loading suppliers.  Please check your database connection.
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  return (
    <DashboardLayout title="Suppliers" subtitle="Manage supplier information">
      <div className="space-y-6">
        {/* Header with Button */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold text-slate-900">
              All Suppliers ({(suppliers || []).length})
            </h2>
          </div>
          <Button
            onClick={handleAddSupplier}
            className="bg-emerald-600 hover:bg-emerald-700 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Supplier
          </Button>
        </div>

        {/* Suppliers Table */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Contact Person
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Address
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {!suppliers || suppliers.length === 0 ? (
                  <tr>
                    <td
                      colSpan={5}
                      className="px-6 py-8 text-center text-slate-500"
                    >
                      No suppliers found.  Add your first supplier to get started.
                    </td>
                  </tr>
                ) : (
                  suppliers.map((supplier) => (
                    <tr key={supplier.id} className="hover:bg-slate-50 transition">
                      <td className="px-6 py-4 text-sm font-medium text-slate-900">
                        {supplier.name}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {supplier.email || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {supplier.phone || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {supplier.contact_person || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {supplier.address || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm space-x-2 flex">
                        <button
                          onClick={() => handleEditSupplier(supplier)}
                          className="p-2 hover:bg-blue-100 rounded-lg transition text-blue-600"
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteSupplier(supplier.id)}
                          disabled={deleteMutation.isPending}
                          className="p-2 hover:bg-red-100 rounded-lg transition text-red-600 disabled: opacity-50"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Supplier Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              {editingId ? "Edit Supplier" : "Add New Supplier"}
            </DialogTitle>
            <DialogDescription>
              {editingId
                ? "Update the supplier information below."
                : "Fill in the details to create a new supplier."}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            {validationErrors.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <ul className="text-sm text-red-700 space-y-1">
                  {validationErrors.map((error, index) => (
                    <li key={index}>• {error}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Supplier Name */}
            <div className="space-y-2">
              <Label htmlFor="name" className="text-sm font-medium">
                Supplier Name *
              </Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter supplier name"
                className="border-slate-200"
              />
            </div>

            {/* Email (optional) */}
            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email
              </Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Enter email address"
                className="border-slate-200"
              />
            </div>

            {/* Phone */}
            <div className="space-y-2">
              <Label htmlFor="phone" className="text-sm font-medium">
                Phone Number *
              </Label>
              <Input
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                placeholder="Enter phone number"
                className="border-slate-200"
              />
            </div>

            {/* Contact Person */}
            <div className="space-y-2">
              <Label htmlFor="contact_person" className="text-sm font-medium">
                Contact Person
              </Label>
              <Input
                id="contact_person"
                name="contact_person"
                value={formData.contact_person}
                onChange={handleInputChange}
                placeholder="Enter contact person (optional)"
                className="border-slate-200"
              />
            </div>

            {/* Address */}
            <div className="space-y-2">
              <Label htmlFor="address" className="text-sm font-medium">
                Address *
              </Label>
              <Textarea
                id="address"
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                placeholder="Enter supplier address"
                className="border-slate-200"
                rows={3}
              />
            </div>
          </div>

          {/* Dialog Actions */}
          <div className="flex justify-end space-x-2">
            <Button
              variant="outline"
              onClick={handleDialogClose}
              disabled={isSubmitting}
            >
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="bg-emerald-600 hover:bg-emerald-700"
            >
              {isSubmitting ? "Saving..." : editingId ? "Update" : "Create"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </DashboardLayout>
  );
}