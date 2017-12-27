const puppeteer = require('puppeteer')
var query = require('./mysql_pool');

(async () => {
  global.browser = await puppeteer.launch({executablePath: 'E:/chromium/chrome.exe', headless: false})
  query('SELECT num_id,title FROM items where pid = 16 ORDER BY comp DESC LIMIT 10', function (err, rows, fields) {
    rows.forEach(function (value, index, arr) {
      similars(value['title'], value['num_id'])
    })
  })
})()

var similars = async function (title, num_id) {
  var page = await browser.newPage()
  let userAgent = 'user-agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
  await page.setUserAgent(userAgent)
  let customHeaders = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://s.taobao.com',
    'upgrade-insecure-requests': '1'
  }
  await page.setExtraHTTPHeaders(customHeaders)
  await page.setViewport({width: 1920, height: 1000})

  // var title = '主推+2017秋冬新款+加绒加厚牛仔外套+8246+8886+P165+控价228'
  // var num_id = '561414769781'

  await page.goto('https://s.taobao.com', {waitUntil: 'domcontentloaded'})
  await page.waitFor('input[name=q]')
  await page.type('input[name=q]', title, {delay: 50})
  await page.click('button[type="submit"]', {delay: 50})

  await page.waitFor(`#J_Itemlist_PLink_${num_id}`)

  var similarHandle = await page.xpath(`//a[@id='J_Itemlist_PLink_${num_id}']/../..//div[@class='similars']//a[1]`)
  var similar_href = await page.evaluate(node => node.href, similarHandle)
  await page.setContent(`<a target="_self" href="${similar_href}">similars</a>`)
  await page.click('a')
  page.on('load', async () => {
    await page.waitFor('a[data-value=sale-desc]')
    await page.click('a[data-value=sale-desc]', {delay: 50})
    await page.waitFor('.filter__item--active a[data-value=sale-desc]')
    var shops = await page.evaluate(() => {
      var anchors = Array.from(document.querySelectorAll('.recitem'))
      return anchors.map(function (anchor) {
        return [
          anchor.querySelector('.info__itemanchor').href.match('[1-9][0-9]{4,}')[0],
          anchor.querySelector('.img__inner').src.replace('_80x80.jpg', ''),
          anchor.querySelector('.info__itemanchor').textContent.replace(/^\s+|\s+$/g, ''),
          anchor.querySelector('.info1__shoplink').textContent.replace(/^\s+|\s+$/g, ''),
          parseFloat(anchor.querySelector('.info2__price').textContent.replace(/^\s+|\s+$/g, '').replace('￥', '')),
          anchor.querySelector('.info2__loc').textContent.replace(/^\s+|\s+$/g, ''),
          parseInt(anchor.querySelector('.info3__npaid').textContent.replace(/^\s+|\s+$/g, '').replace('人付款', '')),
          parseInt(anchor.querySelector('.info3__ncomments .count') == null ? 0 : anchor.querySelector('.info3__ncomments .count').textContent.replace(/^\s+|\s+$/g, '')),
          anchor.querySelector('.info3__ncomments a') == null ? '' : anchor.querySelector('.info3__ncomments a').href,
          JSON.stringify(Array.from(anchor.querySelectorAll('.feature-dsr-list span')).map((dsr) => dsr.textContent.replace(/^\s+|\s+$/g, ''))),
          JSON.stringify(Array.from(anchor.querySelectorAll('.recitem__info5 a')).map((dsr) => dsr.title))
        ]
      })
    })
    await page.close()
    shops.forEach(function (item, index, arr) {
      query(`SELECT id FROM similars where origin_id = '${num_id}' and num_id= '${item[0]}'`, function (err, rows, fields) {
        if (rows.length === 0) {
          query(`INSERT INTO similars (origin_id,num_id,picture,title,seller_nick,price,location,pay_num,rate_num,rate_url,dsr,safe) 
            VALUES ('${num_id}','${item[0]}','${item[1]}','${item[2]}','${item[3]}','${item[4]}','${item[5]}','${item[6]}','${item[7]}','${item[8]}','${item[9]}','${item[10]}')`, function (err, rows, fields) { if (err) throw err })
        } else {
          query(`UPDATE similars SET picture='${item[1]}' ,title='${item[2]}' ,seller_nick='${item[3]}' ,price='${item[4]}' ,location='${item[5]}' ,pay_num='${item[6]}' ,rate_num='${item[7]}' ,rate_url='${item[8]}' ,dsr='${item[9]}' ,safe='${item[10]}' WHERE origin_id = '${num_id}' and num_id= '${item[0]}'`, function (err, rows, fields) { if (err) throw err })
        }
      })
    })
  })
}
