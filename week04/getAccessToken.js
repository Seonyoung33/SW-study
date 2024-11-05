import { useEffect } from 'react';
import axios from 'axios';

const AuthHandler = () => {
    const getAccessToken = async (code) => {
        try {
            const response = await axios.post(
                'https://kauth.kakao.com/oauth/token',
                {
                    grant_type: 'authorization_code',
                    client_id: 'YOUR_REST_API_KEY',
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
        } catch (error) {
            console.error('Failed to fetch access token or send to server', error);
        }
    };

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        if (code) {
            getAccessToken(code);
        }
    }, []);

    return <div>로그인 처리 중...</div>;
};

export default AuthHandler;
