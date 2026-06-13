import DashboardLayout from "@/components/DashboardLayout";
import { Button } from "@/components/ui/button";
import { AlertCircle, Check, Loader2 } from "lucide-react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface OutOfStockItem {
  id: number;
  medicine_id: number;
  medicine_name: string;
  manufacturer: string;
  supplier_name: string;
  supplier_email: string;
  batch_id: string;
  quantity: number;
  expiry_date: string;
  price: number;
}

export default function OutOfStock() {
  // Get user role from localStorage
  const userRole = (() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    return user.role;
  })();
  const isAdmin = userRole === "ADMIN";

  const [selectedItem, setSelectedItem] = useState<OutOfStockItem | null>(null);
  const [requestQuantity, setRequestQuantity] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [requestStatus, setRequestStatus] = useState<"idle" | "success" | "error">("idle");
  
  const { data: outOfStock, isLoading, error, refetch } = useQuery<OutOfStockItem[]>({
    queryKey: ["out-of-stock"],
    queryFn: async () => {
      const response = await fetch("/api/inventory/out-of-stock");
      if (!response.ok) throw new Error("Failed to fetch out of stock items");
      return response.json();
    },
    // Refetch every 10 seconds and when window is focused
    refetchInterval: 10000,
    refetchOnWindowFocus: true,
  });

  const requestMutation = useMutation({
    mutationFn: async () => {
      if (!selectedItem || !requestQuantity) {
        throw new Error("Please enter a quantity");
      }

      const response = await fetch("/api/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("auth_token") || ""}`,
        },
        body: JSON.stringify({
          medicine_id: selectedItem.medicine_id,
          supplier_id: selectedItem.supplier_name, // Using supplier name as reference
          quantity: parseInt(requestQuantity),
          type: "restock",
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Failed to create request");
      }

      return response.json();
    },
    onSuccess: () => {
      setRequestStatus("success");
      setRequestQuantity("");
      setTimeout(() => {
        setIsDialogOpen(false);
        setRequestStatus("idle");
        setSelectedItem(null);
        refetch();
      }, 2000);
    },
    onError: () => {
      setRequestStatus("error");
      setTimeout(() => {
        setRequestStatus("idle");
      }, 3000);
    },
  });

  const handleOpenRequest = (item: OutOfStockItem) => {
    setSelectedItem(item);
    setRequestQuantity("");
    setRequestStatus("idle");
    setIsDialogOpen(true);
  };

  const handleSubmitRequest = () => {
    requestMutation.mutate();
  };

  if (isLoading) {
    return (
      <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-600">Loading out of stock items...</div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
        <div className="flex items-center justify-center h-64">
          <div className="text-red-600">Error loading out of stock items. Please check your database connection.</div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
      <div className="space-y-6">
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <p className="text-sm font-medium text-red-900">
              Total Out of Stock Items: {(outOfStock || []).length}
            </p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Supplier
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Drug Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Manufacturer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Batch ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Expiry Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {!outOfStock || outOfStock.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-6 py-8 text-center text-slate-500">
                      No out of stock items found. All medicines are in stock!
                    </td>
                  </tr>
                ) : (
                  outOfStock.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 transition">
                      <td className="px-6 py-4 text-sm text-slate-600">
                        <div>
                          <p className="font-medium">{item.supplier_name || "N/A"}</p>
                          <p className="text-xs text-slate-500">{item.supplier_email || "N/A"}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm font-medium text-slate-900">
                        {item.medicine_name || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.manufacturer || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700">
                          <AlertCircle className="h-3 w-3" />
                          {item.quantity || 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.batch_id || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.expiry_date ? new Date(item.expiry_date).toLocaleDateString() : "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        ₹{Number(item.price || 0).toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <Button
                          onClick={() => handleOpenRequest(item)}
                          className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs px-3 py-1"
                        >
                          Request
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Request Stock Dialog */}
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Request Stock</DialogTitle>
              <DialogDescription>
                Request stock for {selectedItem?.medicine_name} from {selectedItem?.supplier_name || "supplier"}
              </DialogDescription>
            </DialogHeader>

            {requestStatus === "success" ? (
              <div className="flex flex-col items-center justify-center py-8">
                <Check className="h-12 w-12 text-emerald-600 mb-4" />
                <p className="text-center text-slate-900 font-medium">Request submitted successfully!</p>
                <p className="text-center text-sm text-slate-500 mt-1">The supplier has been notified.</p>
              </div>
            ) : requestStatus === "error" ? (
              <div className="flex flex-col items-center justify-center py-8">
                <AlertCircle className="h-12 w-12 text-red-600 mb-4" />
                <p className="text-center text-slate-900 font-medium">Failed to submit request</p>
                <p className="text-center text-sm text-slate-500 mt-1">Please try again.</p>
              </div>
            ) : (
              <>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="quantity">Quantity to Request</Label>
                    <Input
                      id="quantity"
                      type="number"
                      min="1"
                      step="1"
                      value={requestQuantity}
                      onChange={(e) => setRequestQuantity(e.target.value)}
                      placeholder="Enter quantity"
                      className="mt-1"
                    />
                  </div>
                  <div className="bg-slate-50 rounded-lg p-3 text-sm text-slate-600">
                    <p><strong>Supplier:</strong> {selectedItem?.supplier_name || selectedItem?.supplier_email || "N/A"}</p>
                    <p><strong>Current Price:</strong> ₹{selectedItem?.price || 0}</p>
                    <p><strong>Estimated Cost:</strong> ₹{selectedItem && requestQuantity ? (parseInt(requestQuantity) * (selectedItem.price || 0)).toFixed(2) : "0.00"}</p>
                  </div>
                </div>

                <DialogFooter>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setIsDialogOpen(false)}
                    disabled={requestMutation.isPending}
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={handleSubmitRequest}
                    className="bg-emerald-600 hover:bg-emerald-700"
                    disabled={requestMutation.isPending || !requestQuantity}
                  >
                    {requestMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Submitting...
                      </>
                    ) : (
                      "Submit Request"
                    )}
                  </Button>
                </DialogFooter>
              </>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );

  if (isLoading) {
    return (
      <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
        <div className="flex items-center justify-center h-64">
          <div className="text-slate-600">Loading out of stock items...</div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
        <div className="flex items-center justify-center h-64">
          <div className="text-red-600">Error loading out of stock items. Please check your database connection.</div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Out of Stock" subtitle="Track out of stock medicines">
      <div className="space-y-6">
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <p className="text-sm font-medium text-red-900">
              Total Out of Stock Items: {(outOfStock || []).length}
            </p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Supplier
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Drug Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Manufacturer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Batch ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Expiry Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Price
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-900">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {!outOfStock || outOfStock.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-6 py-8 text-center text-slate-500">
                      No out of stock items found. All medicines are in stock!
                    </td>
                  </tr>
                ) : (
                  outOfStock.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 transition">
                      <td className="px-6 py-4 text-sm text-slate-600">
                        <div>
                          <p className="font-medium">{item.supplier_name || "N/A"}</p>
                          <p className="text-xs text-slate-500">{item.supplier_email || "N/A"}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm font-medium text-slate-900">
                        {item.medicine_name || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.manufacturer || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700">
                          <AlertCircle className="h-3 w-3" />
                          {item.quantity || 0}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.batch_id || "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {item.expiry_date ? new Date(item.expiry_date).toLocaleDateString() : "N/A"}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        ₹{Number(item.price || 0).toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <Button
                          onClick={() => handleRequest(item)}
                          className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs px-3 py-1"
                        >
                          Request
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
