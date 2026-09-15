import type { Metadata } from "next";

import "./globals.css";

import { Navigation } from "@/components/Navigation";

export const metadata: Metadata = {
  title: "Taller 1 | Algoritmos Genéticos",
  description:
    "Laboratorio web de algoritmos genéticos aplicado a cuatro problemas de optimización.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>
        <Navigation />
        <main>{children}</main>
        <footer className="footer">
          Taller 1 · Inteligencia Artificial · Algoritmos Genéticos
        </footer>
      </body>
    </html>
  );
}

