import { useEffect, useState } from 'react';
import axios from 'axios';

const AuthHandler = () => {
    const [loading, setLoading] = useState(true); // 로딩 상태 관리
    const [error, setError] = useState(null); // 에러 상태 관리

    const getAccessToken = async (code) => {
        try {
            const response = await axios.post(
                'https://kauth.kakao.com/oauth/token',
                {
                    grant_type: 'authorization_code',
                    client_id: 'YOUR_REST_API_KEY', // 여기에 실제 REST API 키를 입력하세요.
                    redirect_uri: 'http://localhost:3000/auth',
                    code: code,
                }
            );

            const accessToken = response.data.access_token;

            // 서버로 Access Token 전송
            await axios.post(
                'https://your-server-url.com/auth/kakao',
                {},
                { headers: { Authorization: `Bearer ${accessToken}` } }
            );

            // 성공적으로 처리되었으므로 로딩 상태를 false로 설정
            setLoading(false);
        } catch (error) {
            console.error('Failed to fetch access token or send to server', error);
            setError('로그인 실패. 다시 시도해 주세요.'); // 에러 메시지 설정
            setLoading(false);
        }
    };

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        if (code) {
            getAccessToken(code);
        } else {
            setLoading(false); // 코드가 없으면 로딩 종료
        }
    }, []);

    if (loading) {
        return <div>로그인 처리 중...</div>;
    }

    if (error) {
        return <div>{error}</div>; // 에러 메시지 출력
    }

    return <div>로그인 성공!</div>; // 로그인 성공 메시지
};

export default AuthHandler;
