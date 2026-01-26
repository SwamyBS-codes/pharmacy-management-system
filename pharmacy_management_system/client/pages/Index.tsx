import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import { Link } from "react-router-dom";
import {
  ArrowRight,
  BarChart3,
  FileText,
  Package,
  Pill,
  ShieldCheck,
  ShoppingCart,
  Users,
} from "lucide-react";

export default function Index() {
  const navItems = ["Home", "Medicines", "Billing", "Reports", "Profile"];
  const panels = [
    { title: "Inventory", icon: Package, color: "from-emerald-500 to-teal-500" },
    { title: "Billing", icon: FileText, color: "from-sky-500 to-blue-500" },
    { title: "Sales", icon: BarChart3, color: "from-amber-500 to-orange-500" },
    { title: "Customers", icon: Users, color: "from-indigo-500 to-purple-500" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-sky-50 text-slate-900">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden py-16 sm:py-24">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute -left-32 top-10 h-72 w-72 rounded-full bg-emerald-200 blur-3xl opacity-30" />
          <div className="absolute right-0 bottom-0 h-80 w-80 rounded-full bg-sky-200 blur-3xl opacity-40" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(16,185,129,0.08),transparent_45%),radial-gradient(circle_at_80%_0%,rgba(59,130,246,0.07),transparent_35%)]" />
        </div>

        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full bg-white/80 border border-white/60 px-4 py-2 shadow-sm backdrop-blur">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                Live pharmacy control center
              </div>
              <h1 className="text-4xl sm:text-5xl font-bold leading-tight text-slate-900">
                Your complete pharmacy management solution.
              </h1>
              <p className="text-lg text-slate-600 max-w-2xl">
                Manage inventory, billing, sales, and customers in a tactile, glassy interface with real-time insights and AI-driven alerts.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link to="/signup">
                  <Button className="h-12 px-6 bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-xl shadow-emerald-500/30">
                    Launch Dashboard
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" className="h-12 px-6 border-slate-200 text-slate-800">
                    Sign In
                  </Button>
                </Link>
              </div>
              <div className="flex items-center gap-3 text-sm text-slate-600">
                <ShieldCheck className="h-5 w-5 text-emerald-600" />
                Secure JWT auth • Audit-ready • Role-based access
              </div>
            </div>

            {/* 3D Hero Stage */}
            <div className="relative">
              <div className="absolute -inset-10 rounded-[32px] bg-white/20 backdrop-blur-xl border border-white/40 shadow-[0_20px_80px_rgba(16,185,129,0.12)]" />
              <div
                className="relative rounded-[28px] bg-white/80 backdrop-blur-xl border border-white/70 shadow-2xl p-6 sm:p-8"
                style={{ perspective: "1400px" }}
              >
                <div className="grid gap-6">
                  <div className="grid sm:grid-cols-[1.2fr_0.8fr] gap-6">
                    <div className="relative rounded-3xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white p-6 shadow-xl shadow-emerald-500/30 transform-gpu rotate-1 hover:-rotate-1 transition duration-500">
                      <p className="text-sm opacity-90">Real-time counter</p>
                      <h3 className="text-2xl font-semibold mt-2">Live Billing Desk</h3>
                      <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
                        <div className="rounded-2xl bg-white/15 p-3">
                          <p className="text-xs opacity-80">Queue</p>
                          <p className="text-lg font-semibold">8 active</p>
                        </div>
                        <div className="rounded-2xl bg-white/15 p-3">
                          <p className="text-xs opacity-80">Avg. wait</p>
                          <p className="text-lg font-semibold">2m 14s</p>
                        </div>
                      </div>
                      <div className="absolute -right-4 -bottom-4 h-20 w-20 rounded-full bg-white/15 blur-2xl" />
                    </div>
                    <div className="rounded-3xl bg-white/70 border border-white/60 shadow-lg p-5 transform-gpu -rotate-2 hover:rotate-0 transition duration-500">
                      <p className="text-sm text-slate-600">Shelf view</p>
                      <div className="mt-3 space-y-3">
                        {["Amoxicillin", "Atorvastatin", "Metformin"].map((item, idx) => (
                          <div key={item} className="flex items-center justify-between rounded-2xl bg-gradient-to-r from-slate-50 to-white border border-slate-100 px-4 py-3 shadow-sm">
                            <div className="flex items-center gap-3">
                              <div className="h-10 w-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-semibold">
                                {idx + 1}
                              </div>
                              <div>
                                <p className="font-semibold text-slate-900">{item}</p>
                                <p className="text-xs text-slate-500">Batch ready • In stock</p>
                              </div>
                            </div>
                            <span className="text-sm font-semibold text-emerald-600">★ 4.{idx + 5}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="grid sm:grid-cols-4 gap-4">
                    {panels.map((panel) => (
                      <div
                        key={panel.title}
                        className="group rounded-2xl bg-white/80 border border-white/70 shadow-lg p-4 transform-gpu hover:-translate-y-2 hover:shadow-2xl transition duration-300"
                        style={{ perspective: "800px" }}
                      >
                        <div className={`h-11 w-11 rounded-xl bg-gradient-to-br ${panel.color} text-white flex items-center justify-center shadow-md shadow-black/10`}>
                          <panel.icon className="h-5 w-5" />
                        </div>
                        <p className="mt-3 text-sm font-semibold text-slate-800">{panel.title}</p>
                        <p className="text-xs text-slate-500">Tap to open</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Glass Feature Grid */}
      <section className="pb-20">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-10">
            <div>
              <p className="text-sm font-semibold text-emerald-700">Pharmacy control center</p>
              <h2 className="text-3xl font-bold text-slate-900 mt-2">Deep visibility across every lane</h2>
            </div>
            <Link to="/dashboard" className="hidden sm:inline-flex items-center gap-2 text-emerald-700 font-semibold hover:text-emerald-800">
              Open dashboard <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-2 rounded-3xl bg-white/70 backdrop-blur border border-white/60 shadow-2xl p-6 sm:p-8">
              <div className="flex items-center gap-3 mb-4">
                <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white flex items-center justify-center">
                  <Pill className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm text-slate-600">Inventory & Shelf Health</p>
                  <h3 className="text-xl font-semibold text-slate-900">Live stock, expiry, and reorder radar</h3>
                </div>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                {["Out-of-stock alerts", "Expiry watchlist", "AI reorder guide"].map((item) => (
                  <div key={item} className="rounded-2xl bg-slate-50 border border-slate-100 p-4 shadow-sm">
                    <p className="text-sm font-semibold text-slate-800">{item}</p>
                    <p className="text-xs text-slate-500 mt-2">Stay ahead with predictive signals.</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-3xl bg-white/70 backdrop-blur border border-white/60 shadow-2xl p-6 sm:p-8 flex flex-col justify-between">
              <div>
                <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-sky-500 to-blue-500 text-white flex items-center justify-center mb-3">
                  <ShoppingCart className="h-5 w-5" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900">Billing & POS</h3>
                <p className="text-sm text-slate-600 mt-2">Swift checkout, prescription validation, and digital invoices.</p>
              </div>
              <div className="mt-6 rounded-2xl bg-gradient-to-br from-sky-50 to-blue-50 border border-slate-100 p-4 shadow-inner">
                <p className="text-sm font-semibold text-slate-800">Recent invoices</p>
                <p className="text-xs text-slate-500">Tap to drill down by batch and prescriber.</p>
              </div>
            </div>
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-3">
            <div className="rounded-3xl bg-white/70 backdrop-blur border border-white/60 shadow-2xl p-6 sm:p-8">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 text-white flex items-center justify-center mb-3">
                <BarChart3 className="h-5 w-5" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Sales & Forecasts</h3>
              <p className="text-sm text-slate-600 mt-2">AI-backed 30-day forecasts and seasonal demand signals.</p>
            </div>
            <div className="rounded-3xl bg-white/70 backdrop-blur border border-white/60 shadow-2xl p-6 sm:p-8">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 text-white flex items-center justify-center mb-3">
                <Users className="h-5 w-5" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Customers & Prescriptions</h3>
              <p className="text-sm text-slate-600 mt-2">Profiles, history, and compliance-friendly prescription tracking.</p>
            </div>
            <div className="rounded-3xl bg-white/70 backdrop-blur border border-white/60 shadow-2xl p-6 sm:p-8">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 text-white flex items-center justify-center mb-3">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Security & Compliance</h3>
              <p className="text-sm text-slate-600 mt-2">Role-based access, audit-ready logs, and encrypted data at rest.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
