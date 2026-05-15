export default function TimelineItem({ author, time, content }: { author: string; time: string; content: string }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-slate-900">{author}</p>
          <p className="text-xs text-slate-500">{time}</p>
        </div>
        <div className="h-8 w-8 rounded-full bg-slate-200 text-center leading-8 text-sm font-semibold text-slate-700">{author.charAt(0)}</div>
      </div>
      <p className="mt-3 text-sm leading-6 text-slate-700">{content}</p>
    </div>
  );
}
