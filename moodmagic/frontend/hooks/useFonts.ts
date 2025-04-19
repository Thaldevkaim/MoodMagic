import { useState, useEffect } from 'react';

interface FontPair {
  heading: string;
  body: string;
}

export const useFonts = (fonts: FontPair[]) => {
  const [fontsLoaded, setFontsLoaded] = useState(false);

  useEffect(() => {
    if (!fonts || fonts.length === 0) return;

    const fontPair = fonts[0];
    const headingFont = fontPair.heading.replace(/\s+/g, '+');
    const bodyFont = fontPair.body.replace(/\s+/g, '+');

    // Create a link element for the fonts
    const link = document.createElement('link');
    link.href = `https://fonts.googleapis.com/css2?family=${headingFont}:wght@400;700&family=${bodyFont}:wght@400;500;600&display=swap`;
    link.rel = 'stylesheet';

    // Add the link to the document head
    document.head.appendChild(link);

    // Set up a listener for when the fonts are loaded
    const checkFonts = () => {
      if (document.fonts) {
        Promise.all([
          document.fonts.load(`1em ${fontPair.heading}`),
          document.fonts.load(`1em ${fontPair.body}`)
        ]).then(() => {
          setFontsLoaded(true);
        });
      } else {
        // Fallback for browsers that don't support document.fonts
        setTimeout(() => setFontsLoaded(true), 1000);
      }
    };

    // Check fonts after a short delay to allow for loading
    const timeoutId = setTimeout(checkFonts, 100);

    // Cleanup
    return () => {
      clearTimeout(timeoutId);
      document.head.removeChild(link);
    };
  }, [fonts]);

  return fontsLoaded;
}; 