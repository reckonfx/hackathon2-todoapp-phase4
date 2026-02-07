/**
 * Login page for the Phase-2 Web-Based Todo Application.
 * Full-screen centered login with Black & Gold theme.
 */

import React from 'react';
import Head from 'next/head';
import Login from '../components/Auth/Login';

const LoginPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Login - Todo Premium</title>
        <meta name="description" content="Sign in to your Todo Premium workspace" />
      </Head>
      <Login />
    </>
  );
};

export default LoginPage;
