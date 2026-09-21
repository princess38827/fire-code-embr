import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Embr — Fire Code Playground",
  description: "Explore the provenance-aware Fire Code compiler pipeline.",
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>
}
