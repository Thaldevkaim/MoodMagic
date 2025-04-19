import html2pdf from 'html2pdf.js';

interface ExportOptions {
  filename?: string;
  title?: string;
  subtitle?: string;
}

export const exportMoodboardToPDF = (
  elementId: string,
  options: ExportOptions = {}
) => {
  const element = document.getElementById(elementId);
  if (!element) {
    console.error('Element not found for PDF export');
    return;
  }

  const opt = {
    margin: 10,
    filename: options.filename || 'moodboard.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { 
      scale: 2,
      useCORS: true,
      letterRendering: true
    },
    jsPDF: { 
      unit: 'mm', 
      format: 'a4', 
      orientation: 'portrait' 
    },
    pagebreak: { mode: ['avoid-all'] }
  };

  // Add title and subtitle if provided
  if (options.title || options.subtitle) {
    const titleElement = document.createElement('div');
    titleElement.style.textAlign = 'center';
    titleElement.style.marginBottom = '20px';
    
    if (options.title) {
      const h1 = document.createElement('h1');
      h1.textContent = options.title;
      h1.style.fontSize = '24px';
      h1.style.marginBottom = '10px';
      titleElement.appendChild(h1);
    }
    
    if (options.subtitle) {
      const h2 = document.createElement('h2');
      h2.textContent = options.subtitle;
      h2.style.fontSize = '18px';
      h2.style.color = '#666';
      titleElement.appendChild(h2);
    }

    element.insertBefore(titleElement, element.firstChild);
  }

  // Generate PDF
  html2pdf().set(opt).from(element).save().then(() => {
    // Remove the title element after export
    if (options.title || options.subtitle) {
      const titleElement = element.firstChild;
      if (titleElement) {
        element.removeChild(titleElement);
      }
    }
  });
}; 