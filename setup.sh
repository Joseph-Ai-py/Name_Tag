#!/bin/bash

# NameTag 개발 환경 초기화 및 실행 스크립트

set -e

echo "🚀 NameTag 개발 환경 시작..."

# 백엔드 설정
echo ""
echo "📦 백엔드 준비 중..."
cd backend

if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사합니다."
    cp .env.example .env
    echo "💡 GEMINI_API_KEY를 .env에 설정하세요."
fi

if [ ! -d "venv" ]; then
    echo "🐍 Python 가상환경 생성 중..."
    python -m venv venv
fi

source venv/Scripts/activate 2>/dev/null || . venv/bin/activate
pip install -r requirements.txt -q

cd ..

# 프론트엔드 설정
echo ""
echo "📦 프론트엔드 준비 중..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📥 npm 패키지 설치 중..."
    npm install
fi

cd ..

echo ""
echo "✅ 준비 완료!"
echo ""
echo "개발 서버 시작:"
echo "  터미널 1: cd backend && python -m uvicorn main:app --reload"
echo "  터미널 2: cd frontend && npm run dev"
echo ""
