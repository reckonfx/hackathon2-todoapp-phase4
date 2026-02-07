import type { AppProps } from 'next/app';
import '../styles/globals.css';
import { ThemeProvider } from '../context/ThemeContext';
import { ChatBubbleWidget } from '../components/chat';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider>
      <Component {...pageProps} />
      <ChatBubbleWidget />
    </ThemeProvider>
  );
}

export default MyApp;