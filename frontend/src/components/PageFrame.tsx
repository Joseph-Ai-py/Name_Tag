import type { ReactNode } from "react";

type Props = {
  eyebrow: string;
  title: string;
  description: string;
  children?: ReactNode;
  footer?: ReactNode;
};

export function PageFrame({ eyebrow, title, description, children, footer }: Props) {
  return (
    <div className="space-y-5 rounded-[2rem] border border-stone-200 bg-white/85 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.07)] backdrop-blur md:p-7">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">{eyebrow}</p>
        <h2 className="mt-2 text-3xl font-black tracking-tight text-stone-900 md:text-4xl">{title}</h2>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-stone-600 md:text-base">{description}</p>
      </div>

      <div>{children}</div>

      {footer && <div className="border-t border-stone-200 pt-5">{footer}</div>}
    </div>
  );
}
