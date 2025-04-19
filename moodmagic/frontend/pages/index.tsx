import { useState } from 'react';
import Head from 'next/head';
import MoodboardForm from '../components/MoodboardForm';
import MoodboardPreview from '../components/MoodboardPreview';

export default function Home() {
  const [moodboard, setMoodboard] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Head>
        <title>MoodMagic - Create Your Moodboard</title>
        <meta name="description" content="Create beautiful moodboards with AI" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4 font-display">
              MoodMagic
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Create stunning moodboards with AI-powered inspiration and design recommendations
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <MoodboardForm onMoodboardCreate={setMoodboard} />
            <MoodboardPreview moodboard={moodboard} />
          </div>
        </div>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
          MoodMagic
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <MoodboardForm onMoodboardCreate={setMoodboard} />
          <MoodboardPreview moodboard={moodboard} />
        </div>
      </main>
    </div>
  );
} 