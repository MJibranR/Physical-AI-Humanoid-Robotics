import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Chatbot from '../components/RAGChatbot'; // Import the Chatbot component
import ChapterCards from '../components/ChapterCards'; // Import the new component
import Translate from '@docusaurus/Translate';

import styles from './index.module.css';

function HomepageHeader() {
  // ... (content of HomepageHeader remains the same as previously modified)
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          <Translate>Physical AI & Humanoid Robotics — Essentials</Translate>
        </Heading>
        <p className="hero__subtitle">
          <Translate>A comprehensive guide to building intelligent physical systems</Translate>
        </p>
        <div className={styles.buttonGroup}>
          <Link
            className="button button--primary button--lg"
            to="/docs/book-toc">
            <Translate>GET STARTED</Translate>
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide to building intelligent physical systems">
      <HomepageHeader />
      <main>
        <ChapterCards />
      </main>
      <Chatbot />
    </Layout>
  );
}
