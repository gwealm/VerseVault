import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "@/components/theme/theme-provider";
import { MainNav } from "@/components/nav/main-nav";
import { Footer } from "@/components/footer/footer";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });
const bodyAttrs: string = " min-h-screen flex flex-col";

export const metadata: Metadata = {
    title: "VerseVault",
    description: "Search engine for lyrics",
    icons: "/versevault-logo.png",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={inter.className + bodyAttrs }>
                <ThemeProvider
                    attribute="class"
                    defaultTheme="system"
                    enableSystem
                    disableTransitionOnChange
                >
                        <div className="flex-grow grid grid-cols-1 grid-rows-1">
                            <div>
                                <MainNav />
                                {children}
                            </div>
                        </div>
                        <div>
                            <Footer />
                        </div>
                </ThemeProvider>
            </body>
        </html>
    );
}
