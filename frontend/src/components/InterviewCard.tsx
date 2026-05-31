import { useEffect, useMemo, useRef, useState } from "react";

type InterviewQuestion = {
  question_text: string;
  options: string[];
};

type Props = {
  questions: InterviewQuestion[];
  reasoning: string;
  onComplete: (formattedText: string) => void;
};

export function InterviewCard({ questions, reasoning, onComplete }: Props) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const completedRef = useRef(false);

  useEffect(() => {
    setCurrentIndex(0);
    setAnswers([]);
    completedRef.current = false;
  }, [questions]);

  const currentQuestion = questions[currentIndex];

  const formattedQuestions = useMemo(
    () =>
      questions
        .map((question, index) => `${index + 1}. ${question.question_text}\nA: ${answers[index] || ""}`)
        .join("\n\n"),
    [answers, questions],
  );

  useEffect(() => {
    if (!questions.length || completedRef.current) return;
    if (answers.length === questions.length && answers.every(Boolean)) {
      completedRef.current = true;
      onComplete(formattedQuestions);
    }
  }, [answers, formattedQuestions, onComplete, questions.length]);

  if (!questions.length) {
    return (
      <div className="rounded-3xl border border-stone-200 bg-stone-50 p-6 text-stone-600">
        질문이 아직 생성되지 않았습니다.
      </div>
    );
  }

  return (
    <div className="space-y-5 rounded-3xl border border-stone-200 bg-white p-6 shadow-[0_24px_70px_rgba(15,23,42,0.06)] md:p-8">
      <div className="rounded-2xl bg-amber-50 p-4 text-sm leading-6 text-amber-900">
        <p className="font-semibold">AI 분석</p>
        <p className="mt-2 whitespace-pre-line text-amber-950/80">{reasoning}</p>
      </div>

      <div className="rounded-2xl border border-stone-200 bg-stone-50 p-4">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-semibold text-stone-500">
            질문 {currentIndex + 1} / {questions.length}
          </p>
          <p className="text-xs text-stone-400">4지선다 · 순차 응답</p>
        </div>
        <h3 className="text-xl font-bold leading-snug text-stone-900 md:text-2xl">{currentQuestion.question_text}</h3>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {currentQuestion.options.map((option) => {
          const stripped = option.replace(/^\d+\.\s*/, "");
          const active = answers[currentIndex] === stripped;

          return (
            <button
              key={option}
              type="button"
              onClick={() => {
                const nextAnswers = [...answers];
                nextAnswers[currentIndex] = stripped;
                setAnswers(nextAnswers);
                if (currentIndex < questions.length - 1) {
                  setCurrentIndex((value) => value + 1);
                }
              }}
              className={`rounded-2xl border px-4 py-4 text-left text-sm leading-6 transition ${
                active
                  ? "border-amber-500 bg-amber-50 text-amber-900 shadow-sm"
                  : "border-stone-200 bg-white text-stone-700 hover:border-amber-300 hover:bg-amber-50/40"
              }`}
            >
              {stripped}
            </button>
          );
        })}
      </div>

      {answers.length > 0 && (
        <div className="rounded-2xl border border-stone-200 bg-stone-50 p-4 text-sm text-stone-600">
          <p className="font-semibold text-stone-900">현재 응답 기록</p>
          <pre className="mt-2 overflow-x-auto whitespace-pre-wrap leading-6">{formattedQuestions}</pre>
        </div>
      )}
    </div>
  );
}
