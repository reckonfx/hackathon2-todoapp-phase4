/**
 * Register page for the Phase-2 Web-Based Todo Application.
 * Full-screen centered registration with Black & Gold theme.
 */

import React from 'react';
import Head from 'next/head';
import Register from '../components/Auth/Register';

const RegisterPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>Create Account - Todo Premium</title>
        <meta name="description" content="Join Todo Premium for free today" />
      </Head>
      <Register />
    </>
  );
};

export default RegisterPage;
