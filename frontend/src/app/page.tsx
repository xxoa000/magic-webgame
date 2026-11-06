"use client";

import { useState } from "react";


export default function Home() {
	const [status, setStatus] = useState("확인 전");
	
	async function checkHealth() {
		// 요청 전에 화면 문구 변경
		setStatus("확인 중");

		try {
			// 백엔드에 요청하고 응답을 기다림
			const response = await fetch("http://localhost:8002/health");

			// HTTP 응답이 성공 상태인지 확인
			if (!response.ok) {
				throw new Error("서버 응답 오류");
			}
			// 응답 본문을 JS 값으로 변환
			const data = await response.json();
			// {"status":"ok"} 에서 "ok" 를 꺼내 화면에 반영
			setStatus(data.status);

		} catch {
			setStatus("연결 실패");
		}
	}


    return (
        <main>
            <h1>서버 연결 테스트</h1>
			<button onClick={checkHealth}>서버 연결 확인</button>
            <p>서버 상태: {status}</p>
        </main>
    );
}