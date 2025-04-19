import React, { useState } from 'react';

interface MoodboardFormProps {
  onGenerate: (data: { vibeText: string; selectedTags: string[] }) => void;
}

const TAGS = [
  'Luxury',
  'Retro',
  'Minimal',
  'Earthy',
  'Y2K',
  'Futuristic',
  'Organic',
  'Playful',
  'Dark'
];

export const MoodboardForm: React.FC<MoodboardFormProps> = ({ onGenerate }) => {
  const [vibeText, setVibeText] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const handleTagClick = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate({ vibeText, selectedTags });
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto space-y-8">
      {/* Vibe Text Input */}
      <div className="space-y-2">
        <label 
          htmlFor="vibeText" 
          className="block text-sm font-medium text-gray-700"
        >
          Describe Your Vibe
        </label>
        <textarea
          id="vibeText"
          value={vibeText}
          onChange={(e) => setVibeText(e.target.value)}
          placeholder="Describe your vibe or mood..."
          className="w-full px-4 py-3 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none h-32"
          required
        />
      </div>

      {/* Tags Selection */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Select Tags
        </label>
        <div className="flex flex-wrap gap-2">
          {TAGS.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => handleTagClick(tag)}
              className={`px-4 py-2 text-sm font-medium rounded-full transition-colors duration-200
                ${selectedTags.includes(tag)
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full px-6 py-3 text-base font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
      >
        Generate Moodboard
      </button>
    </form>
  );
}; 