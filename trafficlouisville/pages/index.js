import Head from "next/head";
import Layout from "src/components/Layout";
import Section from "src/components/Section";
import Container from "src/components/Container";
import Map from "src/components/Map";
import Button from "src/components/Button";
import styles from "src/styles/Home.module.scss";
import React from "react";

const DEFAULT_CENTER = [38.2469, -85.7664];

export async function getServerSideProps() {
    try {
        const response = await fetch(`${process.env.DOMAIN_NAME}/${process.env.API_ENDPOINT}`);
        const trafficData = await response.json();

        return { props: { trafficData } };
    } catch (error) {
        console.error("Error fetching traffic data:", error);
        return { props: { trafficData: [] } }; // Return empty array on error
    }
}

export default function Home({ trafficData }) {
    return (
        <Layout>
            <Head>
                <title>TrafficLouisville</title>
                <meta name="description" content="See heatmaps of traffic in Louisville with KYTC camera data" />
                <link rel="icon" href="/trafficlight.ico" />
            </Head>

            <Section>
                <Container>
                    <Map
                        className={styles.homeMap}
                        width="800"
                        height="400"
                        center={DEFAULT_CENTER}
                        zoom={12}
                        trafficData={trafficData}
                    />

                    <p className={styles.description}>
                        This is a research/experimental effort. For authoritative real-time traffic information, please go to{" "}
                        <a href="https://goky.ky.gov/" target="_blank" rel="noopener noreferrer" style={{ color: "blue", textDecoration: "underline" }}>
                            GoKY
                        </a>.
                    </p>

                    <p className={styles.view}>
                        <Button href="https://github.com/browjor/FA24_Capstone_SoMuchForSubtlety.git">View Project on GitHub</Button>
                    </p>
                </Container>
            </Section>
        </Layout>
    );
}
