import Head from 'next/head';

import Header from 'src/components/Header';
import Footer from 'src/components/Footer';

import styles from './Layout.module.scss';
import React from 'react';

const Layout = ({ children, className, ...rest }) => {
  return (
    <div className={styles.layout}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <main className={styles.main}>{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;
