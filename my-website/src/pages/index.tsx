import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import ChapterCards from '../components/ChapterCards'; // Import the new component

import styles from './index.module.css';

function HomepageHeader() {
  // ... (content of HomepageHeader remains the same as previously modified)
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Physical AI & Humanoid Robotics — Essentials
        </Heading>
        <p className="hero__subtitle">A comprehensive guide to building intelligent physical systems</p>
        <div className={styles.buttonGroup}>
          <Link
            className="button button--primary button--lg"
            to="/docs/book-toc">
            GET STARTED
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
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <ChapterCards />
      </main>
    </Layout>
  );
}
