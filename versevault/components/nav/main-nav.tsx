import Link from "next/link";

import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Search } from "../search/search";
import { ModeToggle } from "../theme/mode-toggle";

export function MainNav({
    className,
    ...props
}: React.HTMLAttributes<HTMLElement>) {
    return (
        <div className="hidden flex-col md:flex">
            <div className="flex h-16 items-center px-4 border-b dark:border-b-gray-500">
                <div className="mx-6">
                    <nav
                        className={cn(
                            "flex items-center space-x-4 lg:space-x-6",
                            className
                        )}
                        {...props}
                    >
                        <div className="flex items-center">
                            <div className="flex-shrink-0 mr-2">
                                <a href="/">
                                    <Avatar className="h-8 w-8">
                                        <AvatarImage
                                            src="/versevault-logo.png"
                                            alt="@shadcn"
                                        />
                                        <AvatarFallback>VV</AvatarFallback>
                                    </Avatar>
                                </a>
                            </div>
                            <Link
                                href="/"
                                className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
                            >
                                VerseVault
                            </Link>
                        </div>

                        <Link
                            href="/about"
                            className="text-sm font-medium transition-colors hover:text-primary"
                        >
                            About Us
                        </Link>
                        <Link
                            href="/usage"
                            className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
                        >
                            Usage
                        </Link>
                    </nav>
                </div>
                <div className="ml-auto flex items-center space-x-4">
                    <Search />
                    <ModeToggle />
                </div>
            </div>
        </div>
    );
}
