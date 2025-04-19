import React from 'react';

interface FontPair {
  heading: string;
  body: string;
}

interface FontLoaderProps {
  fonts: FontPair[];
}

const FontLoader: React.FC<FontLoaderProps> = ({ fonts }) => {
  if (!fonts || fonts.length === 0) return null;

  const fontPair = fonts[0]; // We only use the first font pair
  const headingFont = fontPair.heading.replace(/\s+/g, '+');
  const bodyFont = fontPair.body.replace(/\s+/g, '+');

  return (
    <link
      href={`https://fonts.googleapis.com/css2?family=${headingFont}:wght@400;700&family=${bodyFont}:wght@400;500;600&display=swap`}
      rel="stylesheet"
    />
  );
};

export default FontLoader; 