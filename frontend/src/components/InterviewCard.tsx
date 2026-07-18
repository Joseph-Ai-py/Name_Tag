import { useEffect, useMemo, useRef, useState } from "react";
import { useBrandStore } from "../store/brandStore";

type InterviewQuestion = {
  question_text: string;
  options: string[];
};

type Props = {
  questions: InterviewQuestion[];
  reasoning: string;
  onComplete: (formattedText: string) => void;
  sectionKey?: string;
};

export function InterviewCard({ questions, reasoning, onComplete, sectionKey }: Props) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [userInputs, setUserInputs] = useState<Record<string, string>>({});
  const [isEditing, setIsEditing] = useState(false);
  const [editingValue, setEditingValue] = useState("");
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewText, setPreviewText] = useState("");
  
  const saveInterviewSnapshot = useBrandStore((s) => s.saveInterviewSnapshot);
  const getInterviewSnapshot = useBrandStore((s) => s.getInterviewSnapshot);

  useEffect(() => {
    setCurrentIndex(0);
    setAnswers([]);
    if (sectionKey && getInterviewSnapshot) {
      try {
        const s = getInterviewSnapshot(sectionKey);
        if (s && s.answers) {
          setAnswers(s.answers || []);
          setCurrentIndex(typeof s.currentIndex === "number" ? s.currentIndex : 0);
          if (s.user_inputs) {
            setUserInputs(s.user_inputs || {});
          }
        }
      } catch (e) {}
    }
  }, [questions, sectionKey, getInterviewSnapshot]);

  const currentQuestion = useMemo(() => {
    return questions[currentIndex] || questions[0];
  }, [questions, currentIndex]);

  const formattedQuestions = useMemo(
    () =>
      questions
        .map((question, index) => `${index + 1}. ${question.question_text}\nA: ${answers[index] || ""}`)
        .join("\n\n"),
    [answers, questions],
  );

  if (!questions.length || !currentQuestion) {
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
        {currentQuestion.options.map((option, idx) => {
          const stripped = option.replace(/^\d+\.\s*/, "");
          const active = answers[currentIndex] === stripped;

          return (
            <div key={`${currentIndex}-${idx}`} className="flex items-stretch gap-2">
              <button
                type="button"
                onClick={() => {
                    const nextAnswers = [...answers];
                    nextAnswers[currentIndex] = stripped;
                    setAnswers(nextAnswers);
                    try {
                      sectionKey && saveInterviewSnapshot && saveInterviewSnapshot(sectionKey, { answers: nextAnswers, currentIndex, user_inputs: userInputs });
                    } catch (e) {}
                }}
                className={`flex-1 rounded-2xl border px-4 py-4 text-left text-sm leading-6 transition ${
                  active
                    ? "border-amber-500 bg-amber-50 text-amber-900 shadow-sm"
                    : "border-stone-200 bg-white text-stone-700 hover:border-amber-300 hover:bg-amber-50/40"
                }`}
              >
                {stripped}
              </button>
            </div>
          );
        })}
        <div>
          {!isEditing ? (
            <button
              type="button"
              onClick={() => {
                setIsEditing(true);
                setEditingValue(answers[currentIndex] || "");
              }}
              className="w-full rounded-2xl border border-stone-200 bg-white px-4 py-4 text-left text-sm leading-6 text-stone-700 transition hover:border-amber-300 hover:bg-amber-50/40"
            >
              직접 입력
            </button>
          ) : (
            <div className="space-y-2">
              <textarea
                value={editingValue}
                onChange={(e) => setEditingValue(e.target.value)}
                className="w-full min-h-[96px] rounded-2xl border border-stone-200 bg-white px-4 py-3 text-sm text-stone-900 outline-none"
                placeholder="직접 입력할 답변을 작성하세요"
              />
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => {
                      const nextAnswers = [...answers];
                      nextAnswers[currentIndex] = editingValue.trim();
                      setAnswers(nextAnswers);
                      setUserInputs((prev) => ({ ...prev, [String(currentIndex)]: editingValue.trim() }));
                      setIsEditing(false);
                      setEditingValue("");
                      try {
                        sectionKey && saveInterviewSnapshot && saveInterviewSnapshot(sectionKey, { answers: nextAnswers, currentIndex, user_inputs: { ...(userInputs || {}), [String(currentIndex)]: editingValue.trim() } });
                      } catch (e) {}
                  }}
                  className="rounded-full bg-amber-500 px-4 py-2 text-sm text-white"
                >
                  저장
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="mt-3 flex items-center justify-between">
        <button
          type="button"
          onClick={() => {
            if (currentIndex === 0) return;
            const prev = currentIndex - 1;
            setCurrentIndex(prev);
          }}
          className="rounded-full border px-4 py-2 text-sm bg-white"
        >
          뒤로
        </button>
        <button
          type="button"
          onClick={() => {
              if (!answers[currentIndex]) return;
              if (currentIndex < questions.length - 1) {
                const next = currentIndex + 1;
                setCurrentIndex(next);
                try {
                  sectionKey && saveInterviewSnapshot && saveInterviewSnapshot(sectionKey, { answers, currentIndex: next, user_inputs: userInputs });
                } catch (e) {}
              } else {
                // 💡 마지막 질문에서 완료 버튼 클릭 시 데이터 전달
                onComplete(formattedQuestions);
              }
          }}
          className="rounded-full bg-amber-500 px-4 py-2 text-sm text-white"
        >
          {currentIndex === questions.length - 1 ? "인터뷰 완료" : "다음"}
        </button>
      </div>
    </div>
  );
}