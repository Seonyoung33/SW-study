import React from 'react';

const KakaoLogin = () => {
    const REST_API_KEY = 'YOUR_REST_API_KEY';
    const REDIRECT_URI = 'http://localhost:3000/auth';

    // 카카오 로그인 요청 URI
    const kakaoURL = `https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code`;

    const handleLogin = () => {
        window.location.href = kakaoURL;
    };

    return (
        <>
            <button onClick={handleLogin}>카카오 로그인</button>
        </>
    );
};

export default KakaoLogin;
