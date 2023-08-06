/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "410d0b8d824f5c1ff7f2ada4df054fa6"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "efcd1a048bd15ef255c757d5400d1e2c"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "6c16872d0e78330627a1ae3ae5b9832f"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "aaa237949204e27f9d5b4af2246acec1"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "edf35273656c2aabe69b2b8e6968dce1"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "51fd156c062c927efb714c2dd9736ac0"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "a9ee2702659ff5e8ac8e4b14de3cb69b"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "b33c4426d905b3784cb2922bbf9bebe1"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "0a0c0c8e40aeb7403e44d28d42e6d274"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "ce44e1af2c0e27fec9ed6b42cbb12a09"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "651dc97b4d3d4f2ae24c3ae3551bc9ea"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "237d23bdc0343a44ca220ff6ddebcecb"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "6c9fcc2783611f4765c30baee637aa51"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "e541f6f98906f57b572f7c060379c778"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "fbcb75f73493784dfa029c10326ad950"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "409900c3681f8a4453a1d8f28702510c"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "70525a3fcca1a760c82e09784e12a1b3"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "960a7ff199b244fa20665ffee952a41e"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "adee4b7b5451f6e03d37044c6a6349c1"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "47d6b9a33bdd9d5c22e501721eae5c1f"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "1fde02c30c9a50580400948670d81490"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "8a9ac6a152d4b586a3b25ca98bd5ad99"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "663475553508affcffb4915c1acdb6f6"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "e8c52c10afbcdaa6a85ec0e297c972d9"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "dd4dcbab7562be7b174d7e19cba94d7d"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "6b98356c0f41a32b1915e4433eebae39"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "c2d6bfbee64f1d63be65f8c73ae754b7"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "04c619d99ea56c0c9dc93633089ad6c8"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "9341fc3449c26c11a21e861c3573ed91"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "d2a4bc5fa7d9091885eaf79ab1f7cace"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "28e255e51e999dc6da0ad3a1dfa13442"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "9d573aa787733c6d8cfc961d27c7626e"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "bec8ed16e0829b4e8a6a72f5d5d1322b"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "971f6e14a0ce0ab68f19ff6820ef2fcc"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "e28192ef9ca75658cc81ed6fba2879be"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "ea7c77822f69cd1899f0fe769fb4c146"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "777158c514c73a395875259578390b1c"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "7335867de23aabba9c9eb97048974928"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "bc3ce8c7ed51eba17de056bff529c1d2"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "68ed90c1a941a5ad237df7eb055791d3"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "65265be7ca3c12d6a3f1ed236ce6ea02"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "b4fa1161c98c4e9949a87ac412e7ee17"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "38103cb28917daad760b5e1855b1073c"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "bf2003a4c1dc1ad7f65f5621bf118cfa"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "0c55d9a0547aee3a0b8424b1da2d7388"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "d4157c4035414410f87ca2529ce3266a"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "db18fb1fc9c51d6189110ce783919e17"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "c928ff62908b35319016ac5d9386a635"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "64f5248ff652f27b2725ebebacbc0b10"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "c42743b07dbdf8d2730f4df82d5f5143"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "40a99f034a8a4a3aff14b3e73818a680"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "613850e740729c58353efcee02f89ab2"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "e2cd7e27ab4822630a5023542dacb568"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "691b14e378bf07afa64ce30d367994e5"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "c80d662cac32227db3b92bf907fdf553"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "f6de10d4f53fe0272aa0899f20024b0e"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "fee8c4cf358cb71c7a4e5468fcea8457"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "b6d07e507bb5f1951869553f09fcd82b"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "624a2ed282342643d7dc616923f855f6"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "5527f27d9b3a02c1145f0deebc857e86"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "0dc517457c988a2b51039210ea51cf02"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "c1d80a9e2db2578a57c7edb0b6a648a4"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "22dc21a6c0afc1b6feb0f72c01d48037"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "2686d7226ff18219ff5b958861c5faf6"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "be7958ef3443b4aa2a1249bc021ab15c"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "eb3572e8114471bc2b637ff613943d09"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "bf9c648b20a5270ef433035a2236251b"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "d2b9d54775e3bdd80c9ddebbd58bca84"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "8c35fff09333d4a44044316973c0c2cb"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "d00037b4ee071d71e29c59bfdb9c63e9"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "c81f37d6ff6627bc82a4c56c2378d796"
  },
  {
    "url": "404.html",
    "revision": "881e6e03f2188f5313e67a3138eef891"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "a85cb4a54ac5005449ffc5ce2afc4bc8"
  },
  {
    "url": "advanced/index.html",
    "revision": "984f277581ff76d6d1f899b177d4e9da"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "89c238e291e9b9f20274ea98cf9df9c1"
  },
  {
    "url": "advanced/permission.html",
    "revision": "c615d4818641f2c2caa22bef5e51567c"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "4ba9b07ff0f817163c8f5788f89329cd"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "b1a76b73770ccf3b9ceb81c232e0995c"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "e433f313ab089cb244a8fd920e9e4777"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "f3727114f801c3b67c7b0b847c5fd1bb"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "a943c8609be8df4528d66be8202455aa"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "7e94dfff692f2f2f3ccda22eebeaab28"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "d455b96959a94b44e060b1247cc0f0ba"
  },
  {
    "url": "api/config.html",
    "revision": "beb481a45c6f440bc49c278e58a14d16"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "24a8278286eeeb705ae3c6a8256681dd"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "22daa94ef6736c644d73c55d874f0b41"
  },
  {
    "url": "api/exception.html",
    "revision": "1013adf86818ed139911e865f1d92fc0"
  },
  {
    "url": "api/index.html",
    "revision": "cc87fbb1940e2f868685a1572a79162a"
  },
  {
    "url": "api/log.html",
    "revision": "bbd39243492fba9edbec2481c628ca81"
  },
  {
    "url": "api/matcher.html",
    "revision": "16956c7cd655c8b8cf0e70082f335170"
  },
  {
    "url": "api/message.html",
    "revision": "7d6a567480f939f31e7c524e61d281e6"
  },
  {
    "url": "api/nonebot.html",
    "revision": "5325483ad0930381f08222f0c1f87e8a"
  },
  {
    "url": "api/permission.html",
    "revision": "79683529df6c63280852e6d2d91527b2"
  },
  {
    "url": "api/plugin.html",
    "revision": "6bc084d8e184794a042cd28cca83e0a8"
  },
  {
    "url": "api/rule.html",
    "revision": "07d2db5d9b4c75b72f5a49d4481ef5a8"
  },
  {
    "url": "api/typing.html",
    "revision": "e45dbb4025fdef4062de132ed8540a35"
  },
  {
    "url": "api/utils.html",
    "revision": "e4a7d899f5fdfa83414419b32353291d"
  },
  {
    "url": "assets/css/0.styles.371e194f.css",
    "revision": "08479179ebbae9149db293d10e3be884"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.2d526a31.js",
    "revision": "d454db08b1761dc8442ce0b2b9365cc6"
  },
  {
    "url": "assets/js/100.e76b1db8.js",
    "revision": "df14b2fce1b4f3d436e4fcb1c3ff51af"
  },
  {
    "url": "assets/js/101.37d4ef0e.js",
    "revision": "000da90f0962ef35533b8c5ba87c2e1b"
  },
  {
    "url": "assets/js/102.fd309b0c.js",
    "revision": "5a41e0cbd62d3494cb508780e5dba482"
  },
  {
    "url": "assets/js/103.cac238fd.js",
    "revision": "0ea055d59c01db00511744d9355b0bde"
  },
  {
    "url": "assets/js/104.1d36fa29.js",
    "revision": "df4115d99a3d9bd002f830fb4006dc92"
  },
  {
    "url": "assets/js/105.b7afc2d9.js",
    "revision": "ec6bbff6339351558b0f52ba1ae52e73"
  },
  {
    "url": "assets/js/106.c6b33e1a.js",
    "revision": "44506481a7465cccd8c358a0cae60b36"
  },
  {
    "url": "assets/js/107.3168f5af.js",
    "revision": "30ae4e119d57bb9f4145428902c00a7c"
  },
  {
    "url": "assets/js/108.47fc760f.js",
    "revision": "42eb20ae365888ffbd7eabfcf831f28c"
  },
  {
    "url": "assets/js/109.9d02dc2f.js",
    "revision": "7f65f02c1c4d6cb72fb5540bfe1e7bf0"
  },
  {
    "url": "assets/js/11.0aec283a.js",
    "revision": "516e86d065b30a9228a1130d74475054"
  },
  {
    "url": "assets/js/110.6a5c983d.js",
    "revision": "9ed01022a296de0ced501c82f758df4a"
  },
  {
    "url": "assets/js/111.68879819.js",
    "revision": "0a2a2c24c3abb406bd343fb579ea0f57"
  },
  {
    "url": "assets/js/112.a009c3e3.js",
    "revision": "135c5be47fc37ba447a7fffe3f3947a6"
  },
  {
    "url": "assets/js/113.660d6c95.js",
    "revision": "3d29a82b77c5cecfb40e8b7d140adc07"
  },
  {
    "url": "assets/js/114.6a07c030.js",
    "revision": "32a6570c6057c8fa9a42458751c4d159"
  },
  {
    "url": "assets/js/115.47066a4b.js",
    "revision": "b02b81ad198cce0c18e11e2502ba5f08"
  },
  {
    "url": "assets/js/116.34bbd3f9.js",
    "revision": "d82dc91bb8887e64ad5f4fc2283256a3"
  },
  {
    "url": "assets/js/117.0ee84308.js",
    "revision": "f83118d567b115f7e64ebb485877967f"
  },
  {
    "url": "assets/js/118.072d2ed1.js",
    "revision": "eb1867e38851a4c5c3bdbf4212c7593f"
  },
  {
    "url": "assets/js/119.43cb90bd.js",
    "revision": "2269a1a76c307379d3c0861276b9f17e"
  },
  {
    "url": "assets/js/12.ada4ed0c.js",
    "revision": "48b7ee5a4f23a974bf17e83ad943c41b"
  },
  {
    "url": "assets/js/120.4af71aa9.js",
    "revision": "f5ba15eadc006f6451039de800e1f2cf"
  },
  {
    "url": "assets/js/121.3e6eab2e.js",
    "revision": "9e3bed0b19503894b05d974050f20f54"
  },
  {
    "url": "assets/js/122.7a413004.js",
    "revision": "7e4bee4d5222254422a528f6bb1550ec"
  },
  {
    "url": "assets/js/123.4bf12088.js",
    "revision": "c0f9454c259ced96b00010d93cb34d37"
  },
  {
    "url": "assets/js/124.85f5a818.js",
    "revision": "cf8bf1ff561c935dc5d73fe350d1220c"
  },
  {
    "url": "assets/js/125.ab359609.js",
    "revision": "cbfb3884ad6af21bbe179adcf01fc88a"
  },
  {
    "url": "assets/js/126.29f4b4f3.js",
    "revision": "8e61951ff7283f34527ff07d174af2ca"
  },
  {
    "url": "assets/js/127.a5658cbf.js",
    "revision": "2127efec6b923f297be2d1a3c788b1d7"
  },
  {
    "url": "assets/js/128.85eadc4a.js",
    "revision": "ea4b50743e345ea8c0e9f6f27778c744"
  },
  {
    "url": "assets/js/129.05795c66.js",
    "revision": "d92932b3cad567569af4b11ecffc17b2"
  },
  {
    "url": "assets/js/13.cae86f08.js",
    "revision": "4f29e42ab7311ecba77bab797e973558"
  },
  {
    "url": "assets/js/130.a3334d68.js",
    "revision": "4921f7fde962e09a6012b11bf8b1adf0"
  },
  {
    "url": "assets/js/131.ecbc259b.js",
    "revision": "f9ec06941d741bb29482cc2d3dd0db58"
  },
  {
    "url": "assets/js/132.97947577.js",
    "revision": "2d6465c31f12eb8bd1639d43a96c0c59"
  },
  {
    "url": "assets/js/133.ab26ce67.js",
    "revision": "32c9666205c604de1fe9956317a800f5"
  },
  {
    "url": "assets/js/134.8b50aefb.js",
    "revision": "988dd78ca83e18e7b8a6f025d28c2616"
  },
  {
    "url": "assets/js/135.bb553da9.js",
    "revision": "62d10da05cba3b522ba6b7908ea38739"
  },
  {
    "url": "assets/js/136.27f3840f.js",
    "revision": "b34518e2f3687eb8b18f276b6eb6a26a"
  },
  {
    "url": "assets/js/137.9e74ccdb.js",
    "revision": "bfe03ca21af34932e2a9c7d86cfda75b"
  },
  {
    "url": "assets/js/138.37a606b8.js",
    "revision": "3c5d31a58ceed6b404653673905327f6"
  },
  {
    "url": "assets/js/139.0c83cd5b.js",
    "revision": "b0ffd1104f9d8c27f538b9111c156a7a"
  },
  {
    "url": "assets/js/14.40645430.js",
    "revision": "0bc7d61c4ea1a2770535ef619daf97c9"
  },
  {
    "url": "assets/js/140.9e8578e9.js",
    "revision": "c128887dae02a40b65a8857dadc8c476"
  },
  {
    "url": "assets/js/141.651e0f27.js",
    "revision": "de198b4d2729dd760bb0a1045e8e2961"
  },
  {
    "url": "assets/js/142.45b7d6e0.js",
    "revision": "5e9c7833f3aa4cade873527b57334e5c"
  },
  {
    "url": "assets/js/143.ea227833.js",
    "revision": "ec09a7f811d7d5dc6e768069c9438c22"
  },
  {
    "url": "assets/js/144.d9a2473f.js",
    "revision": "a0736aa45abeed5d72384ea1273656a8"
  },
  {
    "url": "assets/js/145.40edebc3.js",
    "revision": "83836ccf5b68c55c4993d84f95ed1cd3"
  },
  {
    "url": "assets/js/146.faa84637.js",
    "revision": "ac87da2be829367bebad1e8df79e5f96"
  },
  {
    "url": "assets/js/147.35787bfe.js",
    "revision": "79ae8c508674f9df84b3cf25e7c2aacc"
  },
  {
    "url": "assets/js/148.15fe2ed5.js",
    "revision": "185e52e605b25458d55d0d9816e3fd6c"
  },
  {
    "url": "assets/js/149.79af7853.js",
    "revision": "c4d8e0cdb6bf2945ed9a99466f92505c"
  },
  {
    "url": "assets/js/15.2719dc91.js",
    "revision": "a42d9045155a1f28c5d13a323ce28599"
  },
  {
    "url": "assets/js/150.6c8aba4c.js",
    "revision": "a3bdd317743e6ffb2b524e8664d8abd3"
  },
  {
    "url": "assets/js/151.be77c989.js",
    "revision": "24aee0beab357ff676fca4d09dd4b1ce"
  },
  {
    "url": "assets/js/152.a97b80ec.js",
    "revision": "bec3e404ace088b1fbfe7d47f7327893"
  },
  {
    "url": "assets/js/153.1f41971f.js",
    "revision": "5baa8a5a85e51af1aa203125943dcb19"
  },
  {
    "url": "assets/js/154.e34aadaa.js",
    "revision": "037470ad594476e45c01e7eaaa32333b"
  },
  {
    "url": "assets/js/155.677ef512.js",
    "revision": "131f54aa9c21b877f8369ad95875dbaa"
  },
  {
    "url": "assets/js/156.c436243e.js",
    "revision": "1e39428783b4ef23f3733a13eaaa15d8"
  },
  {
    "url": "assets/js/157.a1d111e4.js",
    "revision": "471063cb1b5e790e26d702259a101d86"
  },
  {
    "url": "assets/js/158.e332156e.js",
    "revision": "721078278684ede3a92b6282ef4fd6e3"
  },
  {
    "url": "assets/js/159.a5e8a74c.js",
    "revision": "8bdb9b803412fabcbcf6dc6841696dc4"
  },
  {
    "url": "assets/js/16.531460cd.js",
    "revision": "4cd133dc74625dce8bd7e1d7e075cadc"
  },
  {
    "url": "assets/js/160.24fa7732.js",
    "revision": "aeb6bd7644eb0e85ef3bddd391bec48d"
  },
  {
    "url": "assets/js/17.e9cdfd31.js",
    "revision": "2cca3353f8ef005b5f69149161ecb972"
  },
  {
    "url": "assets/js/18.75b165ab.js",
    "revision": "2b1008350481102cf9c960f91c16c8c2"
  },
  {
    "url": "assets/js/19.e768bccb.js",
    "revision": "2267d1553cc17777b907ddce815fce49"
  },
  {
    "url": "assets/js/2.9e2d6c06.js",
    "revision": "1e457d6a57e990c8b0812557ace91a12"
  },
  {
    "url": "assets/js/20.b448cbf7.js",
    "revision": "f241f88281c37b9e03cb21e856fc5f20"
  },
  {
    "url": "assets/js/21.2c14a85b.js",
    "revision": "60cbaacaf0c83936528f51deb28b3fc9"
  },
  {
    "url": "assets/js/22.36bf8c31.js",
    "revision": "d66636bdabf76cd7a69065fe32e55788"
  },
  {
    "url": "assets/js/23.c8f6570a.js",
    "revision": "4e1763c8fca6013c4b9b5de17b45d028"
  },
  {
    "url": "assets/js/24.48148f1f.js",
    "revision": "05606c50de57f839390fcdfddcb55286"
  },
  {
    "url": "assets/js/25.65fe0cf6.js",
    "revision": "25ef7b071947271479d5918b7b9d20cb"
  },
  {
    "url": "assets/js/26.be823409.js",
    "revision": "e939072a641d8afe1bcb1b3271a4c3b1"
  },
  {
    "url": "assets/js/27.43694f25.js",
    "revision": "44413edd73269c5fc372db9c79d7b504"
  },
  {
    "url": "assets/js/28.69d80a18.js",
    "revision": "bb0c394baf2c6b510f0aa838348f6ad4"
  },
  {
    "url": "assets/js/29.056638a1.js",
    "revision": "3ba5af812c452f3d683e9f0353e8127c"
  },
  {
    "url": "assets/js/3.d3c911dd.js",
    "revision": "a544e298e23bca602cd07e134bb0c886"
  },
  {
    "url": "assets/js/30.49f1691f.js",
    "revision": "bef21d2e2fcb63d077ecaf62db935653"
  },
  {
    "url": "assets/js/31.ccd02878.js",
    "revision": "241b614b1d46e7117b5c0806df275133"
  },
  {
    "url": "assets/js/32.fd938f53.js",
    "revision": "04c913c7592381474f5c78f0c2d8ce7c"
  },
  {
    "url": "assets/js/33.9ead72e6.js",
    "revision": "677770ce73e0abac29ac8841b105719f"
  },
  {
    "url": "assets/js/34.b4e0763b.js",
    "revision": "3d377177c32d90d124a864cdfab5fe52"
  },
  {
    "url": "assets/js/35.927ba3d0.js",
    "revision": "bc3aad80c30a2a76d659c4435b3c5995"
  },
  {
    "url": "assets/js/36.1a617f8b.js",
    "revision": "41b1274f93f5a13e8bbd150349be762b"
  },
  {
    "url": "assets/js/37.f4c9766e.js",
    "revision": "5d4c593fe7ea8feb1a31c8cc7633cdd7"
  },
  {
    "url": "assets/js/38.fc6a8184.js",
    "revision": "601ac78e42ad6e25ae8932a3514dfb9e"
  },
  {
    "url": "assets/js/39.2fadf61c.js",
    "revision": "7e109bf2eb5986eb96fbea174bc39652"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.b4254ee2.js",
    "revision": "7443dc5ca7c371e4a5200ddcb6dc81a3"
  },
  {
    "url": "assets/js/41.082e5762.js",
    "revision": "5e58a3256e95d017d0d46b0eaa475f36"
  },
  {
    "url": "assets/js/42.6ce56cc1.js",
    "revision": "b4da8d44deb901ac232d992ed29200cb"
  },
  {
    "url": "assets/js/43.7d03c637.js",
    "revision": "b43337bd0e58dc63541e974b9843403e"
  },
  {
    "url": "assets/js/44.4128924c.js",
    "revision": "2d384ab4c43a0cfb89bde2385364c33e"
  },
  {
    "url": "assets/js/45.ac5f147f.js",
    "revision": "a8531994169e13b805b4b6af42e2d0af"
  },
  {
    "url": "assets/js/46.9c8a2fe1.js",
    "revision": "2a10bacf8a9218ed8a933dbc12e239c3"
  },
  {
    "url": "assets/js/47.169840bd.js",
    "revision": "e94d787e3a8be52c9616f89629e3052e"
  },
  {
    "url": "assets/js/48.f91c1460.js",
    "revision": "f7d5584898a3b17f6849e8428f82d394"
  },
  {
    "url": "assets/js/49.292fc28c.js",
    "revision": "5c91da47bfce34bf2a6ca609fe7d4b7d"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.cad42a1c.js",
    "revision": "2d90c28f3495ae083cb2b40e12b51d88"
  },
  {
    "url": "assets/js/51.8157b4d4.js",
    "revision": "d4a6d5f4672f41d1ef4bc853273b0962"
  },
  {
    "url": "assets/js/52.0b8f8265.js",
    "revision": "ac7b9a13cc989b28cc05501b17aca3fb"
  },
  {
    "url": "assets/js/53.4bc75f0d.js",
    "revision": "9e799b9f2904c54084d766f1637d1a27"
  },
  {
    "url": "assets/js/54.515ab73e.js",
    "revision": "fbd3a56c58f71296e9e455eb22879629"
  },
  {
    "url": "assets/js/55.cf78aa87.js",
    "revision": "18487bb92d10ebc65cf9413c8746c46a"
  },
  {
    "url": "assets/js/56.00d32bf9.js",
    "revision": "a9f066a7eff70ca6b25bfc8c72bebf29"
  },
  {
    "url": "assets/js/57.ce14412d.js",
    "revision": "43313a17ddebc40b8ffea071183568b8"
  },
  {
    "url": "assets/js/58.6a05644f.js",
    "revision": "f0f6b2d57b6855c308be5bbe540d54e9"
  },
  {
    "url": "assets/js/59.b6540a20.js",
    "revision": "7ab881bfd23749011099d380c41f4f5f"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.f1b4522a.js",
    "revision": "7c048f671b4138f9bb07c99e81ba1d3f"
  },
  {
    "url": "assets/js/61.1fe70215.js",
    "revision": "fa17c2d2ea32fe8c3c995f9d827b2a42"
  },
  {
    "url": "assets/js/62.966e30f3.js",
    "revision": "a29568f48a98052d4eee75acab242a14"
  },
  {
    "url": "assets/js/63.5756836c.js",
    "revision": "cf91f8a51d190013bd76f4c22b809310"
  },
  {
    "url": "assets/js/64.6d01c18e.js",
    "revision": "0180ecb79bae5071adda3949c85214d3"
  },
  {
    "url": "assets/js/65.1c57175d.js",
    "revision": "de315c1ffd890a63f16cc39f43c1ffd0"
  },
  {
    "url": "assets/js/66.c21a716a.js",
    "revision": "34c74f225e2d3bc4d6354c56a163ef8d"
  },
  {
    "url": "assets/js/67.582bd0db.js",
    "revision": "5d22c27b35e259ae49b0bb173340eb5b"
  },
  {
    "url": "assets/js/68.ac5a7cca.js",
    "revision": "dc544d4436b43b0d3814b6da9578b27b"
  },
  {
    "url": "assets/js/69.e9bb1ba6.js",
    "revision": "a14052059a0b3d775b083cf30a01e296"
  },
  {
    "url": "assets/js/7.95afef53.js",
    "revision": "7a86d8a66df67c34b9e5b371c386a8c8"
  },
  {
    "url": "assets/js/70.3f5ba8fe.js",
    "revision": "95e23fb8640277eff086b57bf4d2c958"
  },
  {
    "url": "assets/js/71.99347c3a.js",
    "revision": "424420254ea4104e1af53d5ec2cd6223"
  },
  {
    "url": "assets/js/72.6e606825.js",
    "revision": "0dc5aeff4a1ff752fb501d313c27ec8b"
  },
  {
    "url": "assets/js/73.db20037f.js",
    "revision": "40826b1727be597d198d7bae351e968b"
  },
  {
    "url": "assets/js/74.b7d4e733.js",
    "revision": "74ca0cf2f7ffe652006ea74923a850de"
  },
  {
    "url": "assets/js/75.7d309119.js",
    "revision": "5ea57a52fdea74bf7fb836498176a92a"
  },
  {
    "url": "assets/js/76.37665051.js",
    "revision": "83c050928044f4661429d2c5e39a0cea"
  },
  {
    "url": "assets/js/77.8bb75d8b.js",
    "revision": "67e4a5b92cc50737219a4aa8b08495de"
  },
  {
    "url": "assets/js/78.75eeb5f2.js",
    "revision": "7e76be7a4ffff12c7f7391f05ab54a78"
  },
  {
    "url": "assets/js/79.aed48532.js",
    "revision": "01269732b683c5fcfba035c665cbc759"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.d4a18245.js",
    "revision": "0c6edbf7b222905c2f013eb32a648a69"
  },
  {
    "url": "assets/js/81.e7d1d20e.js",
    "revision": "e217a9709719fd8f85d22e51b0f78c8f"
  },
  {
    "url": "assets/js/82.8287f12d.js",
    "revision": "00a74746daa6e4324588255c29d0ee6a"
  },
  {
    "url": "assets/js/83.3702ea90.js",
    "revision": "49658dbe8619e4ccd26d01c3208d9b7b"
  },
  {
    "url": "assets/js/84.75466561.js",
    "revision": "928b35819c53246eaa0a5911467ff07c"
  },
  {
    "url": "assets/js/85.4953201a.js",
    "revision": "10baa272ae8400a28e548f50a49e713a"
  },
  {
    "url": "assets/js/86.2fc92029.js",
    "revision": "f20500199914a0b5a2c9cc99d3a8b4dc"
  },
  {
    "url": "assets/js/87.3551eb6e.js",
    "revision": "eeb642e9cc36e7cdca6538478490d45e"
  },
  {
    "url": "assets/js/88.b8e51db7.js",
    "revision": "888eb739b91febd919c652c17864a47d"
  },
  {
    "url": "assets/js/89.6925d991.js",
    "revision": "705e58e44615b9be9275403fa12c13a2"
  },
  {
    "url": "assets/js/9.2979f5fb.js",
    "revision": "21de61771ae67e0a22a4072a6de45369"
  },
  {
    "url": "assets/js/90.f8b83a8b.js",
    "revision": "4eb3de4a790429ee4407e6caae8c01d3"
  },
  {
    "url": "assets/js/91.ac79ecd2.js",
    "revision": "e5a02ad4198c2449a28d2253b8fdef3e"
  },
  {
    "url": "assets/js/92.7cc7b8f8.js",
    "revision": "561316095406d1b670371acd0b8f3802"
  },
  {
    "url": "assets/js/93.15db1853.js",
    "revision": "412e302789fe56c0326c65845b188729"
  },
  {
    "url": "assets/js/94.b475eb1b.js",
    "revision": "bc53d77fd1b24cf2ad407a3a325ef307"
  },
  {
    "url": "assets/js/95.899a3bb7.js",
    "revision": "a5597df844b285ff6d7a76a09d965d0b"
  },
  {
    "url": "assets/js/96.7d4deee6.js",
    "revision": "75452f5e48ba4cf1b06203168ae91308"
  },
  {
    "url": "assets/js/97.069b1e05.js",
    "revision": "8ca2ca51c374cdc41d6f235a617a715e"
  },
  {
    "url": "assets/js/98.92d8b9ee.js",
    "revision": "c9cafcb9872e0a0b805e7363b0792ef2"
  },
  {
    "url": "assets/js/99.926c3064.js",
    "revision": "34c2e3577a00585298f6fe5db6b306d4"
  },
  {
    "url": "assets/js/app.d048cd2c.js",
    "revision": "06cb674721a2464645cb99f9d05f5c9e"
  },
  {
    "url": "changelog.html",
    "revision": "dba44e7bc20a38ee556f66af0a20a899"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "e2a7b000b92efbca480e099b21b0b150"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "ee30185a1a161325b4b84ae66a5002a3"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "6b13064f428e8346fdcedd689e80afdb"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "ca1ea95047b5a2d8b53e8fa77964243e"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "99043935d2c36613c242d1f119595809"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "db60c0f9741bfb01a525be22645eecd2"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "35c7ea608d6cafcd4aa6f1f18fcb9399"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "9776895f6cb19872c5aa54d4d4655394"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "da6a45ae617dd21b9ace0516174c1236"
  },
  {
    "url": "guide/index.html",
    "revision": "f51ad1f7204fb3086be3939931e84a39"
  },
  {
    "url": "guide/installation.html",
    "revision": "927fe2536cb914109ccbab334c1f251b"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "36e70e9cfc80fc788586fcf1d4ab6f2a"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "2d8ff948f385d83a5c63514b2d66a8ee"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "b2535834816fbbf1d3430d117cb170b0"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "aa7415a7b6a44800ac521e807cbb3460"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "0cc48242026b6f32c128c9c6a3d0f37b"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "3ba8b6a131be04e54745ac5b5d4ce4ff"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "19591db85221d9fb8bd9cf4189afc56d"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "5c852cdf19166726ce4b17312aca3a0b"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "e4da64100d19d5f0fdec22376d34d570"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "fa65c5836193d488082b6806aac9c65b"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "deef11292c3f2613d8bd1ee341709930"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "e5b7c9bbbb6fef0c7a7fb610d4620e64"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "69aee402b95e97634bbd5a69581cd66f"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "b0926906a918637b3ebf7e567ab35ce2"
  },
  {
    "url": "next/api/config.html",
    "revision": "3fbfb010aef4fde44724bfc76f0891f8"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "aa69e5ad3335cd404838079c6e44e5f3"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "ac54b49cdb12c6e91a1618414f15c5d8"
  },
  {
    "url": "next/api/exception.html",
    "revision": "5e2f35637f22f0ac64c24c5437591df3"
  },
  {
    "url": "next/api/index.html",
    "revision": "7018056ba965c9d2891f1214ee5da7f3"
  },
  {
    "url": "next/api/log.html",
    "revision": "ad30797537ac844edde43f91b778e67a"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "deadc4dec7fab5ef1781f2bd31e3c857"
  },
  {
    "url": "next/api/message.html",
    "revision": "86b22f62891fc5a49cc32d510aedc4e8"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "4cd180235ee4ced233641ed8185abd6d"
  },
  {
    "url": "next/api/permission.html",
    "revision": "f7c1927e7c2b5bfc738e3e7c4ad518cf"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "b396dcbb052219e816309436bf7f5569"
  },
  {
    "url": "next/api/rule.html",
    "revision": "dc594a9877838e3a753fa978a8434552"
  },
  {
    "url": "next/api/typing.html",
    "revision": "b58204f94404f8a6227957a59c9a2ebe"
  },
  {
    "url": "next/api/utils.html",
    "revision": "1283b388bda38e99e6e0d689b2721707"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "14428ef0dceabbab95b42790980d67c0"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "cc4f5a22ce14af460c74a4806c93c41c"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "4d46b19f91c813a11f8def627779b6e1"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "61d79518121ad84f06bfdffde5d8cf8f"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "d4271b12d422e706a7732ca613457ebe"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "46ecdc24d50c8d909faf9c5b57eae9dd"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "c28d162084a6c13894e95927b76b3022"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "67d8abbe093a075df18899bae2c938d0"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "6a51233fcc96a0da8a59aca517945dcf"
  },
  {
    "url": "next/guide/index.html",
    "revision": "7f725bab94f54798860120f300693db3"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "53a943aaddf6cdef0b63651fbfcbb522"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "6149c75ef335597c137cd6c38e7bfa89"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "37ec306b59543efd4164c70637042c69"
  },
  {
    "url": "next/index.html",
    "revision": "f96d4485d2f8914c3257f3418cf3328c"
  },
  {
    "url": "plugin-store.html",
    "revision": "e45df1a621a44e37d9a104fdf61601b2"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
