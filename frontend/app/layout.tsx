import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Gestión de Proyecto',
  description: 'Sistema interno empresarial de gestión de proyectos y tareas.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
