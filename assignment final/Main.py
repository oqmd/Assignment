# coding:utf-8

import wx
import pandas as pd
from wx.grid import PyGridTableBase
import wx.adv
import matplotlib.pyplot as plt
import seaborn as sns

# create a frame class
class MyFrame(wx.Frame):
    # initialise
    def __init__(self):
        # create new frame
        wx.Frame.__init__(self, None, title="Airbnb Search Software", pos=(20, 20), size=(1400, 800))
        
        # create new panel
        self.panel = wx.Panel(self, -1)

        # create new layout
        self.sizer = wx.GridBagSizer(4, 13)
        self.total_houses = pd.read_csv("listings_dec18.csv")
        self.show_houses = self.total_houses.iloc[:, :]
        
        self.calendar = pd.read_csv("calendar_dec18.csv")
        self.calendar.dropna(inplace=True)
        self.calendar["date"] = pd.to_datetime(self.calendar["date"])
        self.calendar["price"] = self.calendar["price"].apply(lambda x: float(x.replace("$", "").replace(",", "")))
        
        self.reviews = pd.read_csv("reviews_dec18.csv")
        self.reviews.dropna(inplace=True)
        
        self.table_cols = ["id", "listing_url", "name", "state", "city", "neighbourhood", "booking_price", "room_type"]
        self.cleaness_words = ["chaos", "clean", "dirty", "disorder", "disgusting", "tidy"]
        
        suburb_label = wx.StaticText(self.panel, -1, "Suburb")
        min_price_label = wx.StaticText(self.panel, -1, "Min Price")
        max_price_label = wx.StaticText(self.panel, -1, "Max Price")
        check_in_date_label = wx.StaticText(self.panel, -1, "Check-in Date")
        check_out_date_label = wx.StaticText(self.panel, -1, "Check-out Date")
        room_type_label = wx.StaticText(self.panel, -1, "Room Type")
        keyword_label = wx.StaticText(self.panel, -1, "Keyword")
        selected_cleaness_comments_label = wx.StaticText(self.panel, -1, "Selected Cleaness Comments")
        self.total_cleaness_reviews_num_label = wx.StaticText(self.panel, -1, "")
        sorted_label = wx.StaticText(self.panel, -1, "Sorted")
        
        self.suburb_combobox = wx.ComboBox(self.panel, -1, value='all',choices=["all"] + sorted(self.total_houses["neighbourhood"].dropna().unique().tolist()))
        self.min_price_textctrl = wx.TextCtrl(self.panel, -1, style = wx.TE_CENTER)
        self.max_price_textctrl = wx.TextCtrl(self.panel, -1, size=(40, 20), style = wx.TE_CENTER)
        self.check_in_dpc = wx.adv.DatePickerCtrl(self.panel, size=(100, 20), style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)
        self.check_out_dpc = wx.adv.DatePickerCtrl(self.panel, size=(100, 20), style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY)        
        self.room_type_combobox = wx.ComboBox(self.panel, -1, value='all', choices=["all"] + sorted(self.total_houses["room_type"].dropna().unique().tolist()))
        self.keyword_textctrl = wx.TextCtrl(self.panel, -1, size=(40, 20), style=wx.TE_CENTER)
        self.cleaness_combobox = wx.ComboBox(self.panel, -1, value='all', choices=["all"] + self.cleaness_words)
        self.plot_button = wx.Button(self.panel, label='Plot', size=(50, 20))
        self.search_button = wx.Button(self.panel, label='Search', size=(50, 20))
        self.sorted_combobox = wx.ComboBox(self.panel, -1, value='price from high to low', choices=["price from high to low", "price from low to high", "latest"])

        self.house_table = self.generate_table()
        
        self.plot_button.Bind(wx.EVT_BUTTON, self.plot)
        self.search_button.Bind(wx.EVT_BUTTON, self.change_show_houses)
        self.house_table.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.show_detail)
        
        self.sizer.Add(suburb_label, pos=(0, 0), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.suburb_combobox, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(min_price_label, pos=(0, 3), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.min_price_textctrl, pos=(0, 4), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(max_price_label, pos=(0, 5), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.max_price_textctrl, pos=(0, 6), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(check_in_date_label, pos=(0, 7), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.check_in_dpc, pos=(0, 8), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(check_out_date_label, pos=(0, 9), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.check_out_dpc, pos=(0, 10), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(room_type_label, pos=(0, 11), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.room_type_combobox, pos=(0, 12), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(keyword_label, pos=(1, 0), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.keyword_textctrl, pos=(1, 1), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(selected_cleaness_comments_label, pos=(1, 3), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.cleaness_combobox, pos=(1, 5), span=(1, 3), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(self.search_button, pos=(1, 8), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(self.plot_button, pos=(1, 9), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(self.total_cleaness_reviews_num_label, pos=(2, 0), span=(1, 4), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(sorted_label, pos=(2, 10), flag=wx.EXPAND | wx.TOP, border=15)
        self.sizer.Add(self.sorted_combobox, pos=(2, 11), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=10)
        self.sizer.Add(self.house_table, pos=(3, 0), span=(1, 13), flag=wx.EXPAND | wx.TOP, border=10)

        # add layout to panel
        self.panel.SetSizer(self.sizer)

    def generate_table(self):
        colnames = ["Listing ID", "Listing URL", "House Name", "State", "City", "Suburb", "Price", "Room Type"]
        house_table = wx.grid.Grid(self.panel, -1, size=(-1, 600))
        house_table.CreateGrid(1, 8, selmode=wx.grid.Grid.SelectCells)
        house_table.EnableGridLines(True)
        house_table.SetColSize(0, 100)
        house_table.SetColSize(1, 300)
        house_table.SetColSize(2, 250)
        house_table.SetColSize(3, 100)
        house_table.SetColSize(4, 100)
        house_table.SetColSize(5, 100)
        house_table.SetColSize(6, 100)
        house_table.SetColSize(7, 150)
        for i in range(8):
            house_table.SetColLabelValue(i, colnames[i])
        return house_table

    def plot(self, event):
        Plot(self.show_houses).Show()

    def change_show_houses(self, event):
        try:
            suburb = self.suburb_combobox.GetValue()
            min_price = self.min_price_textctrl.GetValue()
            if min_price == "":
                min_price = -1
            else:
                min_price = float(min_price)
            max_price = self.max_price_textctrl.GetValue()
            if max_price == "":
                max_price = float("Inf")
            else:
                max_price = float(max_price)
            check_in_date = pd.to_datetime(str(self.check_in_dpc.GetValue()).split(",")[0])
            check_out_date = pd.to_datetime(str(self.check_out_dpc.GetValue()).split(",")[0])
            if check_out_date <= check_in_date:
                raise Exception
            room_type = self.room_type_combobox.GetValue()
            keyword = self.keyword_textctrl.GetValue()
            cleaness = self.cleaness_combobox.GetValue()
            sorted_by = self.sorted_combobox.GetValue()
        except Exception as e:
            print(e)
            print("The input is invalid！")
            return None
        total_days = (check_out_date-check_in_date).days
        available_calendar = self.calendar[(self.calendar["date"] >= check_in_date) & (self.calendar["date"] < check_out_date) & (self.calendar["price"] >= min_price) & (self.calendar["price"] <= max_price)]
        house_stat = available_calendar["listing_id"].value_counts().reset_index()
        available_house_ids = house_stat.loc[house_stat["listing_id"] == total_days, "index"].tolist()
        available_calendar = available_calendar[available_calendar["listing_id"].isin(available_house_ids)]
        available_calendar = available_calendar[available_calendar["listing_id"].isin(available_house_ids)]
        available_house_infos = available_calendar.groupby("listing_id")["price"].mean().reset_index()
        available_house_infos.columns = ["id", "booking_price"]
        available_houses = pd.merge(available_house_infos, self.total_houses)
        if suburb != "all":
            available_houses = available_houses[available_houses["neighbourhood"] == suburb]
        if room_type != "all":
            available_houses = available_houses[available_houses["room_type"] == room_type]
        if keyword != "":
            available_houses = available_houses[
                available_houses["name"].str.contains(keyword) |
                available_houses["summary"].str.contains(keyword) |
                available_houses["space"].str.contains(keyword) |
                available_houses["description"].str.contains(keyword) |
                available_houses["neighborhood_overview"].str.contains(keyword) |
                available_houses["notes"].str.contains(keyword) |
                available_houses["transit"].str.contains(keyword) |
                available_houses["host_name"].str.contains(keyword) |
                available_houses["host_about"].str.contains(keyword)
            ]
        if cleaness != "all":
            remain_house_ids = []
            for house_id in available_houses["id"].unique():
                house_reviews = self.reviews[self.reviews["listing_id"] == house_id]
                cleaness_reviews = house_reviews[house_reviews["comments"].str.contains(cleaness)]
                if cleaness_reviews.shape[0] > 0:
                    remain_house_ids.append(house_id)
            available_houses = available_houses[available_houses["id"].isin(remain_house_ids)]
            total_clean_review_num = self.reviews[(self.reviews["comments"].str.contains(cleaness)) & (self.reviews["listing_id"].isin(available_houses["id"].tolist()))].shape[0]
            self.total_cleaness_reviews_num_label.SetLabel("Find {} reviews contains {}".format(total_clean_review_num, cleaness))
        else:
            self.total_cleaness_reviews_num_label.SetLabel("")
        if sorted_by == "price from high to low":
            self.show_houses = available_houses.sort_values("booking_price", ascending=False)
        elif sorted_by == "price from low to high":
            self.show_houses = available_houses.sort_values("booking_price")
        else:
            pass
        self.refresh_table()
            
    def refresh_table(self):
        total_rows = self.house_table.GetNumberRows()
        self.house_table.DeleteRows(numRows=total_rows)
        if self.show_houses.shape[0] == 0:
            self.house_table.AppendRows(numRows=1)
        else:
            self.house_table.AppendRows(numRows=self.show_houses.shape[0])
            for row in range(self.show_houses.shape[0]):
                for col in range(8):
                    if col == 6:
                        self.house_table.SetCellValue(row, col, "${:.2f}".format(self.show_houses[self.table_cols[col]].tolist()[row]))
                    else:
                        self.house_table.SetCellValue(row, col, str(self.show_houses[self.table_cols[col]].tolist()[row]))

    def show_detail(self, event):
        row = event.GetRow()
        listing_id = int(self.house_table.GetCellValue(row, 0))
        house_df = self.show_houses[self.show_houses["id"] == listing_id]
        Detail(house_df).Show()
        
# create a frame class
class Detail(wx.Frame):
    # initialise
    def __init__(self, house):
        self.house = house
        self.reviews = pd.read_csv("reviews_dec18.csv")
        self.reviews = self.reviews[self.reviews["listing_id"] == self.house["id"].tolist()[0]]
        
        # create new frame
        wx.Frame.__init__(self, None, title="Airbnb Search Software", pos=(20, 20), size=(1100, 700))

        # create new panel
        self.panel = wx.Panel(self, -1)

        # create new layout
        self.sizer = wx.GridBagSizer(3, 2)
        
        self.show_detail_button = wx.Button(self.panel, label='Show Detail', size=(100, 20))
        self.show_review_button = wx.Button(self.panel, label='Show Review', size=(100, 20))

        self.info_area = wx.TextCtrl(self.panel, -1, size=(1000, 600), style=wx.TE_MULTILINE)
        
        self.show_detail_button.Bind(wx.EVT_BUTTON, self.show_detail)
        self.show_review_button.Bind(wx.EVT_BUTTON, self.show_review)

        self.sizer.Add(self.show_detail_button, pos=(0, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        self.sizer.Add(self.show_review_button, pos=(0, 1), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        self.sizer.Add(self.info_area, pos=(1, 0), span=(1,3), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        # add layout to panel
        self.panel.SetSizer(self.sizer)
        
    def show_detail(self, event):
        detail = ""
        for col in self.house.columns:
            detail += col + ":" + str(self.house[col].tolist()[0]) + "\n\n"
        self.info_area.Clear()
        self.info_area.SetValue(detail)
        
    def show_review(self, event):
        review = ""
        line_no = 1
        for index in self.reviews.index:
            review += "[{}] ".format(line_no) + self.reviews.loc[index, "comments"] + "\n\n"
            line_no += 1
        self.info_area.Clear()
        self.info_area.SetValue(review)


# create a frame class
class Plot(wx.Frame):
    # initialise
    def __init__(self, houses):
        self.houses = houses
        # set image path
        self.image_file = "hist.png"
        # Set image size and sharpness
        plt.figure(figsize=(4, 2.5), dpi=300)
        # Set the axis text size
        plt.tick_params(labelsize=4)
        # draw a histogram
        sns.distplot(self.houses["booking_price"])
        # add title
        plt.title("Distribution of House Price", fontsize=7)
        plt.xlabel("")
        plt.ylabel("")
        # save image
        plt.savefig(self.image_file)

        # create new frame
        wx.Frame.__init__(self, None, title="Airbnb Search Software", pos=(20, 20), size=(850, 550))

        # create new panel
        self.panel = wx.Panel(self, -1)
        # create new layout
        self.sizer = wx.GridBagSizer(1, 1)
        # new iamge
        self.image = self.get_image(self.image_file, ab_width=800, ab_height=500)
        self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, self.image)
        self.sizer.Add(self.bitmap, pos=(0, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=15)
        # add layout to panel
        self.panel.SetSizer(self.sizer)

    def get_image(self, file, aim_width=0, aim_height=0, ab_width=0, ab_height=0):
        # determine the format of the image
        if file.endswith("png"):
            image = wx.Image(file, wx.BITMAP_TYPE_PNG)
        elif file.endswith("jpg"):
            image = wx.Image(file, wx.BITMAP_TYPE_JPEG)

        # if absolute width and height are 0
        if ab_width == 0 and ab_height == 0:
            # get image width and height
            width = image.GetWidth()
            height = image.GetHeight()

            # calculate the zoom ratio
            rate1 = aim_width/width
            rate2 = aim_height/height

            # determine the final zoom ratio
            scale_rate = min(rate1, rate2)
            # zoom image
            image = image.Scale(width*scale_rate, height*scale_rate)
        # if the absolute width and height is not 0
        else:
            image = image.Scale(ab_width, ab_height)
        bitmap = wx.BitmapFromImage(image)
        return bitmap

# main function, program entry
if __name__ == '__main__':
    # create an app
    app = wx.App()
    # create an instance of the window class and display it
    MyFrame().Show()
    # continuous loop
    app.MainLoop()
