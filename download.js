const puppeteer = require('puppeteer')
var fs = require('fs')
const md5 = require('md5')
var mysql = require('promise-mysql')
var pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'jinjun123',
  database: 'soup',
  connectionLimit: 10
})

if (!fs.existsSync('G:/csv')) { fs.mkdirSync('G:/csv') }
if (!fs.existsSync('G:/csv/full')) { fs.mkdirSync('G:/csv/full') }
if (!fs.existsSync('G:/csv/description')) { fs.mkdirSync('G:/csv/description') }
if (!fs.existsSync('html')) { fs.mkdirSync('html') }

(async () => {
  global.browser = await puppeteer.launch({executablePath: 'E:/chromium/chrome.exe', headless: false})
  var rows = await pool.query('SELECT * FROM items WHERE mid=601 order by list_time DESC limit 20')

  rows.forEach(function (row, index, arr) {
    download(row)
  })
})()

var download = async function (row) {
  var xz_id = row['xz_id']
  var store_name = row['store_name']
  var seller_code = row['seller_code']
  var picture = JSON.parse(row['picture'])
  var description = JSON.parse(row['description'])
  var html = '<div class="picture"><img src="' + picture.join('"><img src="') + '"></div><div class="description"><img src="' + description.join('"><img src="') + '"></div>'
  var file_path = `html/${xz_id}.html`
  fs.writeFileSync(file_path, html)

  var path = 'G:/csv/description/' + store_name + '-' + seller_code + '-' + xz_id
  if (!fs.existsSync(path)) { fs.mkdirSync(path) }

 	var page = await browser.newPage()
  page.on('response', async (resp) => {
    var url = resp.url()
    if (url.indexOf('html') === -1) {
      var key = picture.indexOf(url)
      var name = ''
      if (key > -1) {
        name = 'G:/csv/full/' + md5(xz_id + '-' + key) + '.TBI'
      } else {
        key = description.indexOf(url)
        var split = url.split('.')
        name = path + '/' + key + '.' + split[split.length - 1]
      }
      const buffer = await resp.buffer()
      fs.writeFileSync(name, buffer)
    }
  })
  	await page.goto('file:///G:/node/' + file_path)
}
