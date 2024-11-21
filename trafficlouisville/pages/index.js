import Head from 'next/head';

import Layout from 'src/components/Layout';
import Section from 'src/components/Section';
import Container from 'src/components/Container';
import Map from 'src/components/Map';
import Button from 'src/components/Button';

import styles from 'src/styles/Home.module.scss';

const DEFAULT_CENTER = [38.2469, -85.7664]

export default function Home() {
  return (
    <Layout>
      <Head>
        <title>TrafficLouisville</title>
        <meta name="description" content="See heatmaps of traffic in Louisville with KYTC camera data" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Section>
        <Container>
          <h1 className={styles.title}>
            TrafficLouisville
          </h1>

          <Map className={styles.homeMap} width="800" height="400" center={DEFAULT_CENTER} zoom={12}>
            {({ TileLayer, Marker, Popup }) => (
              <>
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                />
                <Marker position={DEFAULT_CENTER}>
                  <Popup>
                    Heck yeah <br /> I got a website
                  </Popup>
                </Marker>
              </>
            )}
          </Map>

          <p className={styles.description}>
            <code className={styles.code}>KYTC Stuff</code>
          </p>

          <p className={styles.view}>
            <Button href="https://github.com/browjor/FA24_Capstone_SoMuchForSubtlety.git">Vew on GitHub</Button>
          </p>
        </Container>
      </Section>
    </Layout>
  )
}
