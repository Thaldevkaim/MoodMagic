import React, { useState } from 'react';
import { MoodboardForm } from '../components/MoodboardForm';
import { MoodboardPreview } from '../components/MoodboardPreview';

interface MoodboardData {
  color_palette: string[];
  font_pairs: Array<{
    heading: string;
    body: string;
  }>;
  headline: string;
  tagline: string;
  image_urls: string[];
}

export default function Home() {
  const [generatedMoodboard, setGeneratedMoodboard] = useState<MoodboardData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async ({ vibeText, selectedTags }: { vibeText: string; selectedTags: string[] }) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/generate-moodboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vibe_text: vibeText,
          tags: selectedTags,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate moodboard');
      }

      const data = await response.json();
      setGeneratedMoodboard(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            MoodMagic
          </h1>
          <p className="text-xl text-gray-600">
            Transform your creative vision into a stunning moodboard
          </p>
        </div>

        <div className="max-w-3xl mx-auto space-y-12">
          <MoodboardForm onGenerate={handleGenerate} />

          {isLoading && (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent"></div>
              <p className="mt-4 text-gray-600">Generating your moodboard...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {generatedMoodboard && (
            <MoodboardPreview
              colorPalette={generatedMoodboard.color_palette}
              fontPairs={generatedMoodboard.font_pairs}
              headline={generatedMoodboard.headline}
              tagline={generatedMoodboard.tagline}
              imageUrls={generatedMoodboard.image_urls}
            />
          )}
        </div>
      </div>
    </div>
  );
} 