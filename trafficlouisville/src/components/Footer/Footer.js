import Container from 'src/components/Container';

import styles from './Footer.module.scss';

const Footer = ({ ...rest }) => {
  return (
    <footer className={styles.footer} {...rest}>
      <Container className={`${styles.footerContainer} ${styles.footerLegal}`}>
        <p>
          TrafficLouisville, {new Date().getFullYear()}
        </p>
      </Container>
    </footer>
  );
};

export default Footer;
