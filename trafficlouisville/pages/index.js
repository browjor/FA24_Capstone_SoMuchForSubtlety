import Head from "next/head";
import Layout from "src/components/Layout";
import Section from "src/components/Section";
import Container from "src/components/Container";
import Map from "src/components/Map";
import Button from "src/components/Button";
import styles from "src/styles/Home.module.scss";
import React from "react";
import Legend from "src/components/Legend";

const DEFAULT_CENTER = [38.2469, -85.7664];

export async function getServerSideProps() {
    const response = await fetch('https://trafficlouisville.vercel.app/api/traffic');

    if (!response.ok) {
        throw new Error("Failed to fetch traffic data");
    }

    const trafficData = await response.json();
    return { props: { trafficData } };
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
                    <div style={{ background: "white", padding: "20px", borderRadius: "10px", boxShadow: "0 0 10px rgba(0,0,0,0.1)" }}>
                        <p className={styles.title}>
                      This is TrafficLouisville, a capstone project that aims to display traffic densities for Louisville highways, generated from TRIMARC traffic camera images with object detection. All densities shown below are calculated from the number of vehicles detected and a recorded historical maximum. Accidents causing movement of the cameras may lead to inaccurately displayed densities, so please be aware and DRIVE SAFE.
                    </p>
                    </div>

                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
                        {/* Map placed on top */}
                        <Map
                            className={styles.homeMap}
                            width="800"
                            height="400"
                            center={DEFAULT_CENTER}
                            zoom={12}
                            trafficData={trafficData}
                        />
                        {/* Legend placed underneath the map */}
                        <div style={{ marginTop: "10px" }}>
                            <Legend />
                        </div>
                    </div>

                    <p className={styles.description}>
                        This is a research/experimental effort. For authoritative real-time traffic information, please go to{" "}
                        <a
                            href="https://goky.ky.gov/"
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: "blue", textDecoration: "underline" }}
                        >
                            GoKY
                        </a>.
                    </p>

                    <p className={styles.view}>
                        <Button href="https://github.com/browjor/FA24_Capstone_SoMuchForSubtlety.git">
                            View Project on GitHub
                        </Button>
                    </p>
                </Container>
            </Section>
        </Layout>
    );
}
