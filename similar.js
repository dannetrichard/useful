const puppeteer = require('puppeteer')
var mysql = require('promise-mysql');
var pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'jinjun123',
  database: 'soup',
  connectionLimit: 10
});

(async ()=>{
	global.browser = await puppeteer.launch({executablePath: 'E:/chromium/chrome.exe', headless: false})
	var rows = await pool.query('SELECT num_id,title FROM items where pid = 16 ORDER BY comp DESC LIMIT 10')

	for (var i = 0; i < rows.length; i++) {
		si = await similars(rows[i])
		console.log(si)
	}
	await browser.close()
	process.exit()
})()

var similars = async function(row){
	var page = await browser.newPage()
  	var userAgent = 'user-agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
  	await page.setUserAgent(userAgent)
  	var customHeaders = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://s.taobao.com',
    'upgrade-insecure-requests': '1'
  	}
  	await page.setExtraHTTPHeaders(customHeaders)
  	await page.setViewport({width: 1920, height: 1000})

	await page.goto('https://s.taobao.com', {waitUntil: 'domcontentloaded'})
	await page.waitFor('input[name=q]')
	await page.type('input[name=q]', row['title'], {delay: 50})
	await page.click('button[type="submit"]', {delay: 50}) 

	await page.waitFor(`#J_Itemlist_PLink_${row['num_id']}`)
  	var similarHandle = await page.xpath(`//a[@id='J_Itemlist_PLink_${row['num_id']}']/../..//div[@class='similars']//a[1]`)
  	var similar_href = await page.evaluate(node => node.href, similarHandle)
  	await page.setContent(`<a target="_self" href="${similar_href}">similars</a>`)
  	await page.click('a')

	await page.waitFor('a[data-value=sale-desc]')
	await page.click('a[data-value=sale-desc]', {delay: 50})
	await page.waitFor('.filter__item--active a[data-value=sale-desc]')
	var similar_items = await page.evaluate((row) => {
  		var anchors = Array.from(document.querySelectorAll('.recitem'))
  		return anchors.map(function (anchor) {
    		return [
    			  row['num_id'],
		          anchor.querySelector('.info__itemanchor').href.match('[1-9][0-9]{4,}')[0],
		          anchor.querySelector('.img__inner').src.replace('_80x80.jpg', ''),
		          anchor.querySelector('.info__itemanchor').textContent.replace(/^\s+|\s+$/g, '').replace("'",''),
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
	},row)
	await page.close()
	return new Promise(function (resolve, reject) {resolve(similar_items)})
}