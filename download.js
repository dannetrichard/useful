const puppeteer = require('puppeteer')
const fs = require('fs')
const URL = require('url').URL
const md5 = require('md5')
var mysql = require('mysql')

if (!fs.existsSync('G:/csv')) {
  fs.mkdirSync('G:/csv')
}
if (!fs.existsSync('G:/csv/full')) {
  fs.mkdirSync('G:/csv/full')
}
if (!fs.existsSync('G:/csv/description')) {
  fs.mkdirSync('G:/csv/description')
}
if (!fs.existsSync('html')) {
  fs.mkdirSync('html')
}

(async () => {
  global.browser = await puppeteer.launch({executablePath: 'E:/chrome-win32/chrome.exe', headless: false})
  var connection = mysql.createConnection({
    host: '106.14.212.44',
    user: 'root',
    password: 'jinjun123',
    database: 'soup'
  })
  connection.connect()
  connection.query('SELECT xz_id,picture,description,seller_code,store_name from items where store_name = 8307 and mid = 601 limit 10', function (error, rows, fields) {
    if (error) throw error
    rows.forEach(function (value, index, arr) {
      value['picture'] = JSON.parse(value['picture'])
      value['description'] = JSON.parse(value['description'])
      let h1 = '<div class="picture"><img src="' + value['picture'].join('"><img src="') + '"></div>'
      let h2 = '<div class="description"><img src="' + value['description'].join('"><img src="') + '"></div>'
      fs.writeFileSync('html/' + value['xz_id'] + '.html', h1 + h2)
      downloadImgs(value)
    })
  })
  connection.end()
})()


var isHasElement = function (arr, value) {
  for (let i = 0, vlen = arr['picture'].length; i < vlen; i++) {
    if (arr['picture'][i] === value) {
      return ['G:/csv/full', 'G:/csv/full/' + md5(arr['xz_id'] + '-' + i.toString()) + '.TBI']
    }
  }
  for (let i = 0, vlen = arr['description'].length; i < vlen; i++) {
    if (arr['description'][i] === value) {
      let split = value.split('.')
      let path = 'G:/csv/description/' + arr['store_name'] + '-' + arr['seller_code'] + arr['xz_id']
      let name = i + '.' + split[split.length - 1]
      return [path, path + '/' + name]
    }
  }
  return -1
}

var downloadImgs = async function (result) {
  let page = await browser.newPage()
  page.on('response', async (resp) => {
    let url = new URL(resp.url)
    if (url['href'] !== 'file:///G:/node/html/' + result['xz_id'] + '.html') {
      let res = isHasElement(result, url['href'])
      if (res !== -1) {
        if (!fs.existsSync(res[0])) {
          fs.mkdirSync(res[0])
        }
        const buffer = await resp.buffer()
        fs.writeFileSync(res[1], buffer)
      }
    }
  })  
  await page.goto('file:///G:/node/html/' + result['xz_id'] + '.html')
}
