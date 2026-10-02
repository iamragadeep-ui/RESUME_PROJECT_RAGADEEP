const workflowStages = [
  'Triage',
  'Retrieval',
  'Investigation',
  'Validation',
  'Response',
];

export default function HomePage() {
  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="rounded-2xl bg-slate-900 p-6 text-white shadow-lg">
          <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">Delivery Support Resolution Agent</p>
          <h1 className="mt-2 text-3xl font-bold">Customer issue workflow</h1>
        </header>

        <section className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <div className="rounded-2xl bg-white p-6 shadow">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Conversation</h2>
              <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">Agent online</span>
            </div>
            <div className="space-y-4">
              <div className="rounded-xl bg-slate-100 p-4">
                <p className="text-sm text-slate-500">User</p>
                <p className="mt-1">My order was delayed and I need an update. Order ID is ORD-4419.</p>
              </div>
              <div className="rounded-xl bg-cyan-50 p-4">
                <p className="text-sm text-cyan-700">Agent</p>
                <p className="mt-1">I found your shipment is delayed beyond the expected delivery window and I’m checking policy and carrier records before recommending the next step.</p>
              </div>
            </div>
            <div className="mt-6 flex gap-3">
              <input className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none" placeholder="Ask the agent about an order issue" />
              <button className="rounded-xl bg-slate-900 px-5 py-3 font-medium text-white">Send</button>
            </div>
          </div>

          <aside className="space-y-6">
            <div className="rounded-2xl bg-white p-5 shadow">
              <h3 className="text-lg font-semibold">Workflow panel</h3>
              <div className="mt-4 space-y-3">
                {workflowStages.map((stage, index) => (
                  <div key={stage} className={`flex items-center gap-3 rounded-xl p-2 ${index === 2 ? 'bg-cyan-50 text-cyan-700' : 'bg-slate-100 text-slate-700'}`}>
                    <span className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-900 text-xs font-bold text-white">{index + 1}</span>
                    <span>{stage}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl bg-white p-5 shadow">
              <h3 className="text-lg font-semibold">Human approval</h3>
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
                Proposed action: refund review for delayed shipment.
              </div>
              <div className="mt-4 flex gap-3">
                <button className="flex-1 rounded-xl bg-emerald-600 px-3 py-2 text-white">Approve</button>
                <button className="flex-1 rounded-xl bg-red-600 px-3 py-2 text-white">Reject</button>
                <button className="flex-1 rounded-xl bg-slate-200 px-3 py-2">Modify</button>
              </div>
            </div>
          </aside>
        </section>

        <section className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl bg-white p-5 shadow">
            <h3 className="text-lg font-semibold">Sources</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>Order record: ORD-4419</li>
              <li>Tracking record: NS-889456</li>
              <li>Policy: delivery_policy.txt</li>
            </ul>
          </div>

          <div className="rounded-2xl bg-white p-5 shadow">
            <h3 className="text-lg font-semibold">Tool activity</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>get_order() → success</li>
              <li>get_tracking() → success</li>
              <li>create_ticket() → pending</li>
            </ul>
          </div>

          <div className="rounded-2xl bg-white p-5 shadow">
            <h3 className="text-lg font-semibold">Evaluation</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-600">
              <li>Intent accuracy: 0.91</li>
              <li>Groundedness: 0.89</li>
              <li>Latency: 420 ms</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}
