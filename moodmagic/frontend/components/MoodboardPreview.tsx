import { useState, useEffect } from 'react';
import Image from 'next/image';
import { exportMoodboardToPDF } from '../utils/pdfExport';

interface ColorSwatch {
  hex: string;
  name: string;
}

interface MoodboardPreviewProps {
  moodboard: {
    description: string;
    tags: string[];
    createdAt: string;
    colors?: ColorSwatch[];
    fonts?: {
      heading: string;
      body: string;
    };
    headline?: string;
    tagline?: string;
    images?: string[];
    title: string;
    items: {
      id: string;
      type: string;
      url?: string;
      title: string;
      description: string;
    }[];
  } | null;
}

const DEFAULT_COLORS: ColorSwatch[] = [
  { hex: '#2C3E50', name: 'Deep Blue' },
  { hex: '#E74C3C', name: 'Coral Red' },
  { hex: '#ECF0F1', name: 'Cloud White' },
  { hex: '#3498DB', name: 'Sky Blue' },
  { hex: '#2ECC71', name: 'Emerald' },
];

const DEFAULT_FONTS = {
  heading: 'Playfair Display',
  body: 'Inter',
};

export default function MoodboardPreview({ moodboard }: MoodboardPreviewProps) {
  const [colors, setColors] = useState<ColorSwatch[]>(DEFAULT_COLORS);
  const [fonts, setFonts] = useState(DEFAULT_FONTS);
  const [images, setImages] = useState<string[]>([]);

  useEffect(() => {
    if (moodboard) {
      // TODO: Fetch colors, fonts, and images from backend
      // This is just placeholder data
      setColors(moodboard.colors || DEFAULT_COLORS);
      setFonts(moodboard.fonts || DEFAULT_FONTS);
      setImages(moodboard.images || []);
    }
  }, [moodboard]);

  const handleExport = () => {
    exportMoodboardToPDF('moodboard-preview', {
      filename: `${moodboard.title.toLowerCase().replace(/\s+/g, '-')}.pdf`,
      title: moodboard.title,
      subtitle: moodboard.description
    });
  };

  if (!moodboard) {
    return (
      <div className="bg-white p-8 rounded-2xl shadow-lg h-full flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Moodboard Yet</h3>
          <p className="text-gray-500">Create a moodboard to see your design inspiration</p>
        </div>
      </div>
    );
  }

  return (
    <div className="moodboard-preview">
      <div className="moodboard-header">
        <h2>{moodboard.title}</h2>
        <p>{moodboard.description}</p>
        <button 
          onClick={handleExport}
          className="export-button"
        >
          Export as PDF
        </button>
      </div>
      <div id="moodboard-preview" className="moodboard-grid">
        {moodboard.items.map((item) => (
          <div key={item.id} className="moodboard-item">
            {item.type === 'image' ? (
              <img src={item.url} alt={item.title} />
            ) : (
              <div className="text-item">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
} 