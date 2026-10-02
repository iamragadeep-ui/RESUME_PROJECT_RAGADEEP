import './globals.css';

export const metadata = {
  title: 'Delivery Support Resolution Agent',
  description: 'Multi-agent support workflow for order and delivery issues.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
