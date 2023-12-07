/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
          {
            protocol: 'https',
            hostname: 'avatars.githubusercontent.com',
            pathname: '/t/**',
          },
          {
            protocol: 'https',
            hostname: 'lastfm.freetls.fastly.net',
            pathname: '/i/u/**',
          }
        ],
      },
}

module.exports = nextConfig
