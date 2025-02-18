import Link from 'next/link';
import { FaGithub } from 'react-icons/fa';
import Image from 'next/image'; // Import Image component
import React from 'react';

import Container from 'src/components/Container';

import styles from './Header.module.scss';

const Header = () => {
  return (
    <header className={styles.header}>
      <Container className={styles.headerContainer}>
        {/* Logo positioned on the far left */}
        <Link href="/" className={styles.logo}>
          <Image src="/TLlogo.webp" alt="TrafficLouisville Logo" width={60} height={60} />
        </Link>

        {/* Title and navigation */}
        <p className={styles.headerTitle}>TrafficLouisville</p>
        <ul className={styles.headerLinks}>
          <li>
            <a href="https://github.com/browjor/FA24_Capstone_SoMuchForSubtlety.git" target="_blank" rel="noopener noreferrer">
              <FaGithub />
            </a>
          </li>
        </ul>
      </Container>
    </header>
  );
};

export default Header;
