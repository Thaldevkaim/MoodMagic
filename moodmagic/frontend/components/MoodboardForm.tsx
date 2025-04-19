import { useState } from 'react';
import { SparklesIcon } from '@heroicons/react/24/outline';

const VIBE_TAGS = [
  'Luxury', 'Retro', 'Minimal', 'Earthy', 'Y2K', 'Futuristic',
  'Bohemian', 'Industrial', 'Vintage', 'Modern', 'Coastal',
  'Scandinavian', 'Art Deco', 'Mid-Century', 'Contemporary'
];

interface MoodboardFormProps {
  onMoodboardCreate: (moodboard: any) => void;
}

export default function MoodboardForm({ onMoodboardCreate }: MoodboardFormProps) {
  const [description, setDescription] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag)
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    
    try {
      const newMoodboard = {
        description,
        tags: selectedTags,
        createdAt: new Date().toISOString(),
      };

      onMoodboardCreate(newMoodboard);
    } catch (error) {
      console.error('Error creating moodboard:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-2xl shadow-lg">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Create Your Moodboard</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
            Describe your vibe...
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
            placeholder="e.g., A modern, minimalist space with natural elements and warm lighting..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select your style tags
          </label>
          <div className="flex flex-wrap gap-2">
            {VIBE_TAGS.map((tag) => (
              <button
                key={tag}
                type="button"
                onClick={() => toggleTag(tag)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200
                  ${selectedTags.includes(tag)
                    ? 'bg-primary-100 text-primary-800 ring-2 ring-primary-500'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
              >
                {tag}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isGenerating || (!description && selectedTags.length === 0)}
          className={`w-full flex justify-center items-center px-6 py-3 rounded-xl text-lg font-semibold text-white transition-all duration-200
            ${isGenerating || (!description && selectedTags.length === 0)
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 shadow-lg hover:shadow-xl'
            }`}
        >
          <SparklesIcon className="h-6 w-6 mr-2" />
          {isGenerating ? 'Generating...' : 'Generate Moodboard'}
        </button>
      </form>
    </div>
  );
} 