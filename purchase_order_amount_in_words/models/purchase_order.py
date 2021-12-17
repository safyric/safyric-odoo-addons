from odoo import api, fields, models

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'
    
    @api.model
    def Num2MoneyFormat(self, change_number):
        format_word = ["分", "角", "元","拾", "百", "千", "万", "拾", "百", "千", "亿","拾", "百", "千", "万", "拾", "百", "千", "兆"]

        format_num = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]

        if type(change_number) == float:
            real_numbers = []
            for i in range(len(format_word) - 3, -3, -1):
                if change_number >= 10 ** i or i < 1:
                    real_numbers.append(
                        int(round(change_number/(10**i), 2) % 10))

        elif isinstance(change_number, (int, long)):
            real_numbers = [int(i) for i in str(change_number) + '00']

        zflag = 0  # 标记连续0次数，以删除万字，或适时插入零字
        start = len(real_numbers) - 3
        change_words = []
        for i in range(start, -3, -1):  # 使i对应实际位数，负数为角分
            if real_numbers[start-i] <> 0 or len(change_words) == 0:
                if zflag:
                    change_words.append(format_num[0])
                    zflag = 0
                change_words.append(format_num[real_numbers[start - i]])
                change_words.append(format_word[i+2])

            elif 0 == i or (0 == i % 4 and zflag < 3):  # 控制 万/元
                change_words.append(format_word[i+2])
                zflag = 0
            else:
                zflag += 1

        if change_words[-1] not in (format_word[0], format_word[1]):
            # - 最后两位非"角,分"则补"整"
            change_words.append("整")

        return ''.join(change_words)

        @api.multi
        def _compute_amount_in_words(self):
            for rec in self:
                rec.amount_words = str(rec.Num2MoneyFormat(rec.amount_total))

    amount_words = fields.Char(string="金额大写", compute='_compute_amount_in_words')
