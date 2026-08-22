import './globals.css';
import Nav from '../components/Nav.jsx';

export const metadata = {
  title: 'Especialização em Engenharia de Dados',
  description: 'Programa autodirigido de Engenharia de Dados — teoria, prática e portfólio.',
};

const temaInit = `(function(){try{var t=localStorage.getItem('tema');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}})();`;

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Manrope:wght@400;500;600;700&display=swap"
        />
        <script dangerouslySetInnerHTML={{ __html: temaInit }} />
      </head>
      <body>
        <Nav />
        {children}
      </body>
    </html>
  );
}
