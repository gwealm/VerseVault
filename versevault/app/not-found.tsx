import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
    return (
        <>
            <main className="flex flex-col justify-center items-center min-h-screen text-center">
                <div className="max-w-md p-4 mx-auto">
                    <p className="text-2xl font-bold mb-4">
                        404 - Page Not Found
                    </p>
                    <Image
                        alt="VerseVault Logo"
                        src="/versevault-logo.png"
                        width={300}
                        height={300}
                        className="rounded-full mb-4 mx-auto"
                    />
                    <div>
                        <p className="text-lg mb-4">
                            Sorry, the page you are looking for does not exist.
                        </p>
                        <Link href="/" className="text-blue-500">
                            Go back to Home
                        </Link>
                    </div>
                </div>
            </main>
        </>
    );
}