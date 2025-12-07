import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

type ChapterItem = {
  title: string;
  description: string;
  link: string;
  icon: string;
  gradient: string;
};

const ChapterList: ChapterItem[] = [
  {
    title: 'Introduction',
    description: 'Explore the fundamentals of Physical AI and Humanoid Robotics, setting the stage for advanced concepts.',
    link: '/docs/book-toc#introduction',
    icon: '📚',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  {
    title: 'Chapter 1: Robotics Fundamentals',
    description: 'Master the core principles of robotics including mechanics, sensors, actuators, and control systems.',
    link: '/docs/book-toc#chapter-1-robotics-fundamentals',
    icon: '⚙️',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  },
  {
    title: 'Chapter 2: Artificial Intelligence in Robotics',
    description: 'Discover how AI powers modern robotics through machine learning, computer vision, and decision-making algorithms.',
    link: '/docs/book-toc#chapter-2-artificial-intelligence-in-robotics',
    icon: '🧠',
    gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  },
  {
    title: 'Chapter 3: Humanoid Robot Anatomy',
    description: 'Understand the structural design, joint systems, and biomechanics that enable human-like movement.',
    link: '/docs/book-toc#chapter-3-humanoid-robot-anatomy',
    icon: '🦾',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  },
  {
    title: 'Chapter 4: Locomotion and Balance',
    description: 'Learn advanced techniques for bipedal walking, dynamic balance, and stable movement in complex environments.',
    link: '/docs/book-toc#chapter-4-locomotion-and-balance',
    icon: '🚶',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  },
  {
    title: 'Chapter 5: Human-Robot Interaction',
    description: 'Explore natural communication, social robotics, and designing intuitive interfaces for human collaboration.',
    link: '/docs/book-toc#chapter-5-human-robot-interaction',
    icon: '🤝',
    gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
  },
  {
    title: 'Chapter 6: Ethical Considerations',
    description: 'Examine the moral implications, safety protocols, and societal impact of humanoid robotics technology.',
    link: '/docs/book-toc#chapter-6-ethical-considerations',
    icon: '⚖️',
    gradient: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
  },
  {
    title: 'Conclusion',
    description: 'Summarize key learnings, explore future outlooks, and find resources for further reading and research.',
    link: '/docs/book-toc#conclusion',
    icon: '🎯',
    gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
  },
];

function ChapterCard({title, description, link, icon, gradient}: ChapterItem) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <Link to={link} className={clsx('card card--full-height', styles.chapterCard)}>
        <div className="card__header">
          <div className={styles.iconContainer} style={{background: gradient}}>
            <span className={styles.chapterIcon}>{icon}</span>
          </div>
          <Heading as="h3" className={styles.chapterTitle}>{title}</Heading>
        </div>
        <div className="card__body">
          <p className={styles.chapterDescription}>{description}</p>
        </div>
        <div className="card__footer">
          <button className="button button--primary button--block">
            Read More →
          </button>
        </div>
      </Link>
    </div>
  );
}

export default function ChapterCards(): JSX.Element {
  return (
    <section className={clsx('margin-top--lg', styles.chapterCardsContainer)}>
      <div className="container">
        <Heading as="h2" className={clsx('text--center margin-bottom--lg', styles.sectionTitle)}>
          Book Chapters
        </Heading>
        <p className={clsx('text--center margin-bottom--xl', styles.sectionSubtitle)}>
          Explore our comprehensive guide to Physical AI and Humanoid Robotics
        </p>
        <div className="row">
          {ChapterList.map((props, idx) => (
            <ChapterCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}