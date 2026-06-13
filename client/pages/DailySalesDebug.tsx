import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DailySalesDebug() {
  const [refreshCount, setRefreshCount] = useState(0);

  const { data: salesStats, isLoading, refetch } = useQuery({
    queryKey: ["daily-sales-debug"],
    queryFn: async () => {
      console.log("🔄 Fetching daily sales...");
      const response = await api.sales.getStatsSummary();
      console.log("✅ Received:", {
        summary: response.data?.summary,
        dailySales: response.data?.dailySales?.slice(0, 3),
      });
      return response.data;
    },
    staleTime: 0,
  });

  const dailySales = salesStats?.dailySales || [];
  const mostRecent = dailySales[0];
  
  // Find today's specific date
  const todayStr = new Date().toISOString().split('T')[0];
  const todayData = dailySales.find((day: any) => {
    const dayStr = new Date(day.date).toISOString().split('T')[0];
    return dayStr === todayStr;
  });

  useEffect(() => {
    console.log("📊 Daily sales state updated:", { mostRecent, todayData, todayStr });
  }, [mostRecent, todayData]);

  return (
    <DashboardLayout title="Daily Sales Debug" subtitle="Real-time sales tracking">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Manual Refresh Button */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <Button
            onClick={() => {
              console.log("🔄 Manual refresh triggered");
              setRefreshCount(c => c + 1);
              refetch();
            }}
            className="gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Manual Refresh (Count: {refreshCount})
          </Button>
        </div>

        {/* Today's Sales Card */}
        <div className="bg-gradient-to-r from-emerald-50 to-teal-50 rounded-lg shadow-sm border border-emerald-200 p-6">
          <h3 className="text-lg font-semibold text-emerald-900 mb-2">Today's Sales</h3>
          <p className="text-xs text-emerald-700 mb-4">({todayStr})</p>
          {isLoading ? (
            <p className="text-emerald-700">Loading...</p>
          ) : todayData ? (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-emerald-700">Date:</span>
                <span className="font-bold text-emerald-900">{todayData.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-emerald-700">Amount:</span>
                <span className="font-bold text-2xl text-emerald-600">₹{Number(todayData.sales).toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-emerald-700">Transactions:</span>
                <span className="font-bold text-emerald-900">{todayData.transactions}</span>
              </div>
            </div>
          ) : (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
              <p className="text-yellow-700 font-medium">No sales for today yet</p>
              <p className="text-xs text-yellow-600 mt-1">Complete a sale to see it appear here</p>
            </div>
          )}
        </div>

        {/* Most Recent Sale Card */}
        {mostRecent && (
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-sm border border-blue-200 p-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">Most Recent Sale Date</h3>
            <p className="text-xs text-blue-700 mb-4">(Latest in database)</p>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-blue-700">Date:</span>
                <span className="font-bold text-blue-900">{mostRecent.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-blue-700">Amount:</span>
                <span className="font-bold text-2xl text-blue-600">₹{Number(mostRecent.sales).toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-blue-700">Transactions:</span>
                <span className="font-bold text-blue-900">{mostRecent.transactions}</span>
              </div>
            </div>
          </div>
        )}

        {/* Last 5 Days */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Last 5 Days</h3>
          <div className="space-y-3">
            {dailySales.slice(0, 5).map((day: any, idx: number) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
                <div>
                  <p className="font-medium text-slate-900">{day.date}</p>
                  <p className="text-xs text-slate-500">{day.transactions} transactions</p>
                </div>
                <p className="font-bold text-lg text-emerald-600">₹{Number(day.sales).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Raw Data */}
        <div className="bg-slate-50 rounded-lg border border-slate-200 p-6">
          <h3 className="text-sm font-mono text-slate-600 mb-2">Raw Data (Console):</h3>
          <button
            onClick={() => {
              console.log("📊 Full sales stats:", salesStats);
              alert("Check browser console for full data");
            }}
            className="text-blue-600 hover:underline text-sm"
          >
            Log to Console →
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}
