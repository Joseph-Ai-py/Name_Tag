export function LoadingSpinner({ label = "로딩 중..." }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-stone-200 bg-white px-4 py-3 text-stone-700 shadow-sm">
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-stone-200 border-t-amber-500" />
      <span className="text-sm font-medium">{label}</span>
    </div>
  );
}
