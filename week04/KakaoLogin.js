import React, { useEffect } from 'react';

const KakaoLogin = () => {
  useEffect(() => {
    // 카카오 초기화
    window.Kakao.init('REST_API_KEY'); // 카카오 REST API 키
  }, []);

  const handleLogin = () => {
    window.Kakao.Auth.login({
      success: function (authObj) {
        console.log(authObj); // 로그인 성공 시 authObj에 대한 정보가 출력됩니다.
        // 로그인 후 사용자 정보 가져오기
        getUserInfo();
      },
      fail: function (err) {
        console.error(err); // 로그인 실패 시 에러 출력
      },
    });
  };

  const getUserInfo = () => {
    window.Kakao.API.request({
      url: '/v2/user/me',
      success: function (res) {
        console.log(res); // 사용자 정보 출력
      },
      fail: function (err) {
        console.error(err); // 사용자 정보 요청 실패 시 에러 출력
      },
    });
  };

  return (
    <div>
      <button onClick={handleLogin}>카카오 로그인</button>
    </div>
  );
};

export default KakaoLogin;
