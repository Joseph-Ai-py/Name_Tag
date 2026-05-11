import { useMutation } from "@tanstack/react-query";
import { generateBrand, type BrandGenerateParams } from "../lib/api";
import { useGenerationStore } from "../stores/generationStore";

export function useGenerate() {
  const setIsLoading = useGenerationStore((s) => s.setIsLoading);
  const setError = useGenerationStore((s) => s.setError);
  const setResult = useGenerationStore((s) => s.setResult);
  const setStep = useGenerationStore((s) => s.setStep);

  const mutation = useMutation({
    mutationFn: (params: BrandGenerateParams) => generateBrand(params),
    onMutate: () => {
      setIsLoading(true);
      setError(null);
      setStep(4);
    },
    onSuccess: (data) => {
      setResult(data);
      setIsLoading(false);
    },
    onError: (error: any) => {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        "브랜드 생성에 실패했습니다. 다시 시도해주세요.";
      setError(errorMessage);
      setStep(3);
      setIsLoading(false);
    },
  });

  return mutation;
}
