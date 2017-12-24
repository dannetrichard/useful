const puppeteer = require('puppeteer')
var xpath = require('xpath')
var dom = require('xmldom').DOMParser;

(async () => {
  const url = 'https://s.taobao.com'
  const title = '大货已出 保暖真狐狸毛大毛领短款连帽棉衣 6023P165 控价228'
  const wangwang = 'yuting19890106'

  const browser = await puppeteer.launch({executablePath: 'E:/chromium/chrome.exe', headless: false})
  const page = await browser.newPage()
  const userAgent = 'user-agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
  await page.setUserAgent(userAgent)
  const customHeaders = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://s.taobao.com',
    'upgrade-insecure-requests': '1'
  }

  await page.setExtraHTTPHeaders(customHeaders)
  await page.setViewport({width: 1920, height: 1000})
  await page.goto(url, {waitUntil: 'domcontentloaded'})
  await page.waitFor('input[name=q]')

  console.time('hello')
  await page.type('input[name=q]', title)
  await page.click('button[type="submit"]', {delay: 50})

  await page.waitFor('.shopname')
  const names = await page.evaluate(() => {
    const anchors = Array.from(document.querySelectorAll('.shopname'))
    return anchors.map(anchor => anchor.textContent.replace(/^\s+|\s+$/g, ''))
  })

  for (var i in names) {
    if (names[i] == wangwang) {
      i++
      break
    }
  }
  await page.hover(`.item:nth-child(${i}) .pic-box`)
  await page.click(`.item:nth-child(${i}) .similars a`, {delay: 50})

  /*
  await page.waitFor('.items')
  const itemElement = await page.xpath('//div[@class="shop"]/a/span[2]..div[contains(@class,"item")]')
  const itemElement = await itemsElement.xpath('//div[@class="shop"]/a/span[2]..div[contains(@class,"item")]')
  await itemElement.$('.pic-box').hover()
  await itemElement.$('.similars a').click({delay: 50})
  */

  browser.on('targetcreated', async target => {
    let pageSimilar = await target.page()
    await pageSimilar.waitFor('a[data-value=sale-desc]')
    await pageSimilar.click('a[data-value=sale-desc]', {delay: 50})
    await pageSimilar.waitFor('.filter__item--active a[data-value=sale-desc]')
    const shops = await pageSimilar.evaluate(() => {
      const anchors = Array.from(document.querySelectorAll('.recitem'))
      return anchors.map(function (anchor) {
        return [
          anchor.querySelector('.info__itemanchor').href,
          anchor.querySelector('.img__inner').src,
          anchor.querySelector('.info__itemanchor').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info1__shoplink').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info2__price').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info2__loc').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info3__npaid').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info3__ncomments .count') == null ? 0 : anchor.querySelector('.info3__ncomments .count').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info3__ncomments a') == null ? '' : anchor.querySelector('.info3__ncomments a').href,
          Array.from(anchor.querySelectorAll('.feature-dsr-list span')).map((dsr) => dsr.textContent.replace(/^\s+|\s+$/g, '')),
          Array.from(anchor.querySelectorAll('.recitem__info5 a')).map((dsr) => dsr.title)
        ]
      })
    })
    console.log(shops)
    console.timeEnd('hello')
  })
})()
