from odoo import api, fields, models
from datetime import datetime

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def _compute_amount_in_words(self):
        for rec in self:
            rec.amount_words = str(rec._rmb_upper(rec.amount_total))

    def _rmb_upper(self, value):
        """
        人民币大写
        传入浮点类型的值返回 unicode 字符串
        """
        map = [u"零", u"壹", u"贰", u"叁", u"肆", u"伍", u"陆", u"柒", u"捌", u"玖"]
        unit = [u"分", u"角", u"元", u"拾", u"百", u"千", u"万", u"拾", u"百", u"千", u"亿", u"拾", u"百", u"千", u"万", u"拾", u"百", u"千", u"兆"]

        nums = [] # 取出每一位数字，整数用字符方式转换避大数出现误差
        for i in range(len(unit)-3, -3, -1):
            if value >= 10**i or i < 1:
                nums.append(int(round(value/(10**i), 2)) % 10)

        words = []
        zflag = 0 # 标记连续0次数，以删除万字，或适时插入零字
        start = len(nums)-3
        for i in range(start, -3, -1): # 使i对应实际位数，负数为角分
            if 0 != nums[start-i] or len(words) == 0:
                if zflag:
                    words.append(map[0])
                    zflag = 0                    
                    ords.append(map[nums[start-i]])
                    words.append(unit[i+2])
                elif 0 == i or (0 == i % 4 and zflag < 3): # 控制‘万/元’
                    words.append(unit[i+2])
                    zflag = 0
                else:
                    zflag += 1

        if words[-1] != unit[0]: # 结尾非‘分’补整字 words.append(u"整")
            return ''.join(words)

    amount_words = fields.Char(string="金额大写", compute='_compute_amount_in_words')
