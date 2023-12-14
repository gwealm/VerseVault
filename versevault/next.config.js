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
          },
          {
            protocol: 'https',
            hostname: 'cdn-icons-png.flaticon.com',
            pathname: '/512/26/26789.png'
          }
        ],
      },
}

module.exports = nextConfig
